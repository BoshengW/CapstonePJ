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
        user_FavoriteMovieList = getMostPopularMovieList()



    return user_FavoriteMovieList


def getMostPopularMovieList(MovieMetaDB, Top10MovieEachGenresDB, MovieRateCount, MovieAvgRate):
    """
    return top10 most popular movies in each genres
    :return: movieId list
    """
    genres_list = ['(no genres listed)', 'Action', 'Adventure', 'Animation', 'Children',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
       'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
       'War', 'Western']

    dict_movie_eachGenres = {}

    for _genre in genres_list:
        _top10_movieList = Top10MovieEachGenresDB.find_one({'genre': _genre})['Top10Movie']
        _moiveInfolist = []

        for _movieId in _top10_movieList:
            _movieInfo = MovieMetaDB.find_one({'movieId': _movieId})
            ## remove Object ID which is no-serializable
            del _movieInfo['_id']
            _movieInfo['AvgRate'] = MovieAvgRate.find_one({'movieId': _movieId})['avg_rate']
            _movieInfo['RateCount'] = MovieRateCount.find_one({'movieId': _movieId})['count']
            _moiveInfolist.append(_movieInfo)
        dict_movie_eachGenres[_genre] = _moiveInfolist

    dict_movie_eachGenres['GenresList'] = genres_list


    return dict_movie_eachGenres


def getCurrentPopularMovieList(MovieMetaDB, MovieRateCount, MovieAvgRate):
    """
    return top10 most popular movies in CurrentMovieCount MongoDB
    :return:
    """

    return


