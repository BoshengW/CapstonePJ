import json
import random

def findUserFavoriteMovies(rating_dict, ):
    """
    getting user rating_dict -> find rate>3 movielist

    Note: If no rating >3, then we just send most popular as recommendation

    :param rating_dict:
    :return: user high rate movie: rate>3
    """
    user_FavoriteMovieList = []

    for _key in sorted(rating_dict, key=rating_dict.get, reverse=True):
        if rating_dict[_key]>3:
            user_FavoriteMovieList.append(_key)

    if not user_FavoriteMovieList:
        user_FavoriteMovieList = getPopularMovieList();



    return user_FavoriteMovieList


def getPopularMovieList():
    """
    return top10 most popular movies currently
    :return: movieId list
    """
    popular_list = random.sample(range(1,1682), 10)

    return popular_list
