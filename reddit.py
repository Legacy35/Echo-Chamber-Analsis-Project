from psaw import PushshiftAPI

api = PushshiftAPI()

gen = api.search_comments(limit=100)
results = list(gen)