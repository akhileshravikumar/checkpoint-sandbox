"""A tiny query utility. Deliberately under-validated: this is the agent's target."""


def parse_query(query):
    """Split a raw query string into lowercase terms."""
    return query.strip().lower().split()
