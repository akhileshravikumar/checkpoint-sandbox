import pytest

from sandbox.search import parse_query, rank_results, top_n

RESULTS = [
    {"id": 1, "title": "Python packaging guide"},
    {"id": 2, "title": "Guide to Rust"},
    {"id": 3, "title": "Python typing deep dive"},
]


def test_parse_query_splits_and_lowercases():
    assert parse_query("  Python Guide ") == ["python", "guide"]


def test_rank_results_orders_by_score():
    ranked = rank_results(RESULTS, ["python", "guide"])
    assert ranked[0]["id"] == 1
    assert ranked[0]["score"] == 2


def test_top_n_limits():
    assert len(top_n(RESULTS, ["python"], n=2)) == 2