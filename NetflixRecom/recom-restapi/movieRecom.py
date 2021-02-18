import random
import numpy as np
# import faiss

def findUserFavoriteMovies(rating_dict):
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

    ## new user didn't like all movies in cold-start questions, then recom them most popular movie
    if not user_FavoriteMovieList:
        user_FavoriteMovieList = getPopularMovieList()


    return user_FavoriteMovieList


def getPopularMovieList():
    """
    return top10 most popular movies currently
    :return: movieId list
    """
    popular_list = random.sample(range(1,1682), 10)

    return popular_list


def randhomChooseMovies(movie_count):
    """
    this is function randomly choose mutiple movie for new user rating
    @:param
    movies_count
    """
    if movie_count<=1:
        print("movie_count error, please check DB")
        return []
    random_movieId_list = random.sample(range(1, 200), 8)
    return random_movieId_list


def getRatingMatrix(rating_dict, rating_matrix_length):
    """
    get rating matrix based on user ratings
    """

    user_ratingMatrix = np.zeros(rating_matrix_length)

    for _key in rating_dict.keys():
        user_ratingMatrix[int(_key) - 1] = rating_dict[_key]


    return user_ratingMatrix


def newUserFoldinAlgorithm(U_matrix, Sigma, V_matrix, user_ratingMatrix, rating_matrix_length):
    """
    this is function to generate new user-feature for solving cold-start issue
    """
    project_userMatrix = np.dot(np.dot(user_ratingMatrix.reshape(1, rating_matrix_length),
                                       V_matrix.transpose()), Sigma)

    user_count = U_matrix.shape[0]
    _ids = np.array(range(1, user_count + 1)).astype(np.int64)

    ## use faiss framework for online similarity searching
    faiss_index = faiss.IndexFlatL2(U_matrix.shape[1])
    faiss_index2 = faiss.IndexIDMap(faiss_index)
    faiss_index2.add_with_ids(U_matrix, _ids)

    project_userMatrix = project_userMatrix.astype("float32")
    topK = 5
    Score, userIdList = faiss_index2.search(project_userMatrix, topK)

    print(userIdList)

    return userIdList[0]