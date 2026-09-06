"""A tiny query utility, deliberately under-validated. This is the agent target."""


def parse_query(query):
    """Split a raw query string into lowercase terms."""
    return query.strip().lower().split()
