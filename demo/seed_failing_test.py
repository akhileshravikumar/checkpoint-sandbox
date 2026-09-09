"""Appends a test that the current implementation fails.

Used to trigger the CI self-healing loop on demand (W2D10, W3D4).
The gap is real: parse_query has no guard for None or empty input.
"""
from pathlib import Path

FAILING = '''

def test_parse_query_rejects_empty():
    with pytest.raises(ValueError):
        parse_query("   ")


def test_parse_query_rejects_none():
    with pytest.raises(TypeError):
        parse_query(None)
'''

p = Path("tests/test_search.py")
if "rejects_empty" not in p.read_text():
    p.write_text(p.read_text() + FAILING)
    print("seeded failing tests")
else:
    print("already seeded")
