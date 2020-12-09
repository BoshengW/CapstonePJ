import random

def randhomChooseMovies(movie_count):
    """
    this is function randomly choose mutiple movie for new user rating
    @:param
    movies_count
    """
    if movie_count<=1:
        print("movie_count error, please check DB")
        return []
    random_movieId_list = random.sample(range(1, movie_count), 8)
    return random_movieId_list



