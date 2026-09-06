"""A tiny query utility, deliberately under-validated. This is the agent target."""


def parse_query(query):
    """Split a raw query string into lowercase terms."""
    if not query or not query.isalpha():
        raise ValueError("Query must be non-empty and contain only alphabetic characters.")
    return query.strip().lower().split()
