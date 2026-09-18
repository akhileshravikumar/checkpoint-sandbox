"""A tiny query utility, deliberately under-validated. This is the agent target."""


def parse_query(query):
    """Split a raw query string into lowercase terms."""
    if not isinstance(query, str):
        raise ValueError("Input must be a string.")
    return query.strip().lower().split()


def rank_results(results, terms):
    """Score each result by how many query terms appear in its title."""
    scored = []
    for r in results:
        score = sum(1 for t in terms if t in r["title"].lower())
        scored.append({**r, "score": score})
    return sorted(scored, key=lambda r: r["score"], reverse=True)


def top_n(results, terms, n=3):
    """Return the n highest-scoring results."""
    return rank_results(results, terms)[:n]
