"""A task that is already done must end as "no change", not as an error, and
nothing in the prompts may pressure the model into inventing an edit.

Real propose_diff and plan nodes; only the LLM is stubbed, with a script of
responses so each attempt can answer differently.
"""
import sqlite3
import subprocess

import pytest
from langgraph.checkpoint.sqlite import SqliteSaver

from app import graph as graph_mod
from app.nodes import plan as plan_mod
from app.nodes import propose_diff as diff_mod
from app.schemas import ChangePlan

BEFORE = 'def parse_query(q):\n    if not q:\n        raise ValueError("empty")\n    return q.split()\n'
CHANGED = ('def parse_query(q):\n    if not isinstance(q, str):\n        raise TypeError("str")\n'
           '    if not q:\n        raise ValueError("empty")\n    return q.split()\n')
BROKEN = 'def parse_query(q):\n    return """oops\n'
PLAN = ChangePlan(target_file="search.py", summary="Add input validation to parse_query",
                  steps=["Raise ValueError on empty input"], rationale="guard input")


class Msg:
    def __init__(self, content):
        self.content = content
        self.response_metadata = {"done_reason": "stop"}


@pytest.fixture
def llm(monkeypatch):
    """Script the rewrite responses and record every prompt sent."""
    box = {"script": [], "prompts": []}

    class Rewrite:
        def invoke(self, messages):
            box["prompts"].append(messages)
            return Msg(box["script"].pop(0))
        def stream(self, messages):
            yield self.invoke(messages)

    class Plan:
        def with_structured_output(self, *_a, **_k):
            return type("P", (), {"invoke": lambda self, m: PLAN.model_copy()})()

    monkeypatch.setattr(plan_mod, "get_llm", lambda **_k: Plan())
    monkeypatch.setattr(diff_mod, "get_llm", lambda **_k: Rewrite())
    return box


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run(["git", "init", "-q", str(r)], check=True)
    (r / "search.py").write_text(BEFORE)
    return r


def _run(tmp_path, repo, **state):
    saver = SqliteSaver(sqlite3.connect(str(tmp_path / "cp.sqlite"), check_same_thread=False))
    saver.setup()
    graph = graph_mod.build_graph(saver)
    cfg = {"configurable": {"thread_id": "nc"}}
    out = graph.invoke({"task": "add input validation to search.py",
                        "repo_path": str(repo), "retry_count": 0, **state}, config=cfg)
    return graph, cfg, out


def test_already_done_ends_as_no_change(llm, repo, tmp_path):
    llm["script"] = [BEFORE, BEFORE]
    graph, cfg, out = _run(tmp_path, repo)
    assert not out.get("error")
    assert out["no_change_reason"].startswith("No change proposed for search.py")
    assert "Add input validation" in out["no_change_reason"], "show what the plan was"
    assert graph.get_state(cfg).next == (), "the run ends; there is nothing to approve"
    assert (repo / "search.py").read_text() == BEFORE


def test_no_prompt_demands_a_change(llm, repo, tmp_path):
    llm["script"] = [BEFORE, BEFORE]
    _run(tmp_path, repo)
    system = llm["prompts"][0][0][1]
    assert "MUST differ" not in system
    retry_hint = llm["prompts"][1][-1][1]
    assert "return it unchanged again" in retry_hint
    assert "must change" not in retry_hint.lower()


def test_a_lazy_first_answer_still_gets_a_second_chance(llm, repo, tmp_path):
    llm["script"] = [BEFORE, CHANGED]
    _, _, out = _run(tmp_path, repo)
    assert out["__interrupt__"], "a real change on attempt 2 reaches the gate"
    assert not out.get("no_change_reason")
    assert out["rewrite_attempt"] == 2, "METRICS needs to know which attempt won"


def test_unchanged_then_broken_is_an_error_not_no_change(llm, repo, tmp_path):
    llm["script"] = [BEFORE, BROKEN]
    _, _, out = _run(tmp_path, repo)
    assert "not valid Python" in out["error"]
    assert not out.get("no_change_reason")


def test_no_change_on_a_retry_is_an_error(llm, repo, tmp_path):
    """After a CI failure, "no change" leaves a red PR: that must be loud."""
    llm["script"] = [BEFORE, BEFORE]
    _, _, out = _run(tmp_path, repo, retry_count=1,
                     plan=PLAN.model_dump(), ci_failure_log="E   TypeError")
    assert "proposed no change to search.py on retry 1" in out["error"]
    assert not out.get("no_change_reason")

CI_LOG = ("E   AttributeError: 'NoneType' object has no attribute 'strip'\n"
          "FAILED tests/test_search.py::test_parse_query_rejects_none - AttributeError: ...")
TESTS = ("import pytest\nfrom search import parse_query\n\n\n"
         "def test_parse_query_rejects_none():\n    with pytest.raises(TypeError):\n"
         "        parse_query(None)\n")


def test_a_ci_retry_shows_the_rewrite_the_failure_and_the_test(llm, repo, tmp_path):
    """The live bug: the rewrite never saw the CI failure, so it returned the
    file unchanged twice and the retry died as "no change"."""
    (repo / "tests").mkdir()
    (repo / "tests" / "test_search.py").write_text(TESTS)
    llm["script"] = [BEFORE, CHANGED]
    _, _, out = _run(tmp_path, repo, retry_count=1, plan=PLAN.model_dump(),
                     ci_failure_log=CI_LOG)
    assert out["__interrupt__"], "the fix reaches the gate"
    first_user = llm["prompts"][0][1][1]
    assert "FAILED CI" in first_user
    assert "test_parse_query_rejects_none" in first_user
    assert "pytest.raises(TypeError)" in first_user, "the expectation, not just the error"
    assert "requires TypeError from `parse_query(None)`" in first_user, "stated, not inferred"
    hint = llm["prompts"][1][-1][1]
    assert "version that was rejected" in hint
    assert "return it unchanged again" not in hint


def test_an_edit_note_reaches_the_rewrite(llm, repo, tmp_path):
    


def test_a_fresh_task_prompt_has_no_retry_context(llm, repo, tmp_path):
    llm["script"] = [CHANGED]
    _run(tmp_path, repo)
    user = llm["prompts"][0][1][1]
    assert "FAILED CI" not in user and "reviewer" not in user

