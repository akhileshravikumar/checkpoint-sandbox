# """A tiny query utility, deliberately under-validated. This is the agent target."""


# def parse_query(query):
#     """Split a raw query string into lowercase terms."""
#     return query.strip().lower().split()


# def rank_results(results, terms):
#     """Score each result by how many query terms appear in its title.
    
#     This function takes a list of results and a list of query terms. It
#     calculates the score for each result by counting how many of the query
#     terms are present in the result's title. The results are then sorted
#     in descending order based on their scores, and the top n results are
#     returned."""
#      scored = []
#      for r in results:
#         score = sum(1 for t in terms if t in r["title"].lower())


# def top_n(results, terms, n=3):
#     """Return the n highest-scoring results."""
#     return rank_results(results, terms)[:n]

# def parse_query1(query):
#     """Split a raw query string into lowercase terms."""
#     return query.strip().lower().split()


# def rank_results1(results, terms):
#     """Score each result by how many query terms appear in its title.
    
#     This function takes a list of results and a list of query terms. It
#     calculates the score for each result by counting how many of the query
#     terms are present in the result's title. The results are then sorted
#     in descending order based on their scores, and the top n results are
#     returned."""
#      scored = []
#      for r in results:
#         score = sum(1 for t in terms if t in r["title"].lower())


# def top_n1(results, terms, n=3):
#     """Return the n highest-scoring results."""
#     return rank_results1(results, terms)[:n]
    


def parse_query(query):
    """Split a raw query string into lowercase terms."""
    return query.strip().lower().split()
    

def rank_results(results, terms):
    """Score each result by how many query terms appear in its title.
    
    This function takes a list of results and a list of query terms. It
    calculates the score for each result by counting how many of the query
    terms are present in the result's title. The results are then sorted
    in descending order based on their scores, and the top n results are
    returned."""
     scored = []
     for r in results:
        score = sum(1 for t in terms if t in r["title"].lower())


def top_n(results, terms, n=3):
    """Return the n highest-scoring results."""
    return rank_results(results, terms)[:n]


def rank_results1(results, terms):
    """Score each result by how many query terms appear in its title.
    
    This function takes a list of results and a list of query terms. It
    calculates the score for each result by counting how many of the query
    terms are present in the result's title. The results are then sorted
    in descending order based on their scores, and the top n results are
    returned."""
     scored = []
     for r in results:
        score = sum(1 for t in terms if t in r["title"].lower())


def top_n1(results, terms, n=3):
    """Return the n highest-scoring results."""
    return rank_results1(results, terms)[:n]


# """A tiny query utility, deliberately under-validated. This is the agent target."""


# def parse_query(query):
#     """Split a raw query string into lowercase terms."""
#     return query.strip().lower().split()


# def rank_results(results, terms):
#     """Score each result by how many query terms appear in its title.
    
#     This function takes a list of results and a list of query terms. It
#     calculates the score for each result by counting how many of the query
#     terms are present in the result's title. The results are then sorted
#     in descending order based on their scores, and the top n results are
#     returned."""
#      scored = []
#      for r in results:
#         score = sum(1 for t in terms if t in r["title"].lower())


# def top_n(results, terms, n=3):
#     """Return the n highest-scoring results."""
#     return rank_results(results, terms)[:n]

# def parse_query1(query):
#     """Split a raw query string into lowercase terms."""
#     return query.strip().lower().split()


# def rank_results1(results, terms):
#     """Score each result by how many query terms appear in its title.
    
#     This function takes a list of results and a list of query terms. It
#     calculates the score for each result by counting how many of the query
#     terms are present in the result's title. The results are then sorted
#     in descending order based on their scores, and the top n results are
#     returned."""
#      scored = []
#      for r in results:
#         score = sum(1 for t in terms if t in r["title"].lower())


# def top_n1(results, terms, n=3):
#     """Return the n highest-scoring results."""
#     return rank_results1(results, terms)[:n]