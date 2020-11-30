import json

def load_movie_question(path):

    with open(path) as f:
        data = json.load(f)

    return data

