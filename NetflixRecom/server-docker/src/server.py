from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_cors import CORS

from bson.json_util import dumps
from flask_pymongo import PyMongo

from flask import Response
import movieRecom
import numpy as np

import util


app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://root:13820381042bq@recomsys.zqcg8.mongodb.net/LearnMongo?retryWrites=true&w=majority"
mongo = PyMongo(app)
global SVD_users_matrix
global SVD_movies_matrix
global SVD_sigma_matrix



@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/register", methods=['POST'])
def registerUser():

    _registerUser = request.get_json(force=True)

    print(_registerUser)
    _username = _registerUser['username']
    _password = _registerUser['password']
    _email = _registerUser['email']
    _newId = mongo.db.user_login100K.count()+1

    ## First check if user already registered
    _user = mongo.db.user_login100K.find_one({'username': _username})
    if not _user:
        _registerUser2DB = {
            "username": _username,
            "password": _password,
            "email": _email,
            "userId": _newId
        }

        ## check if insertion succeed
        _id = mongo.db.user_login100K.insert_one(_registerUser2DB)

        if not _id:
            return Response(status=203, mimetype="application/json")
        else:
            return Response(status=200, mimetype="application/json")
    else:
        return Response(status=203, mimetype="application/json")




@app.route("/loginInfo", methods=['GET', 'POST'])
def validateUserInfo():

    response = {}

    _loginUser = request.get_json(force=True)
    print(_loginUser)

    # add username and password back to frontend- not recommand
    _user = mongo.db.user_login100K.find_one({'username': _loginUser['username']})
    if not _user:
        print('username not found')
        response['userExist'] = False
        response['newUser'] = ""
        response['username'] = ""
        response['password'] = ""
        response['userId'] = ""

    else:
        response['userExist'] = True
        response['newUser'] = checkNewUserOrNot(_user)
        response['username'] = _user['username']
        response['password'] = _user['password']
        response['userId'] = _user['userId']

    resp = dumps(response)
    print(resp)

    return resp

def checkNewUserOrNot(user):
    _user_features = mongo.db.users_Top5Sim100K.find_one({'userId': user['userId']})
    if not _user_features:
        #this is new user since there is no user-feature matrix
        return True
    else:
        return False



@app.route("/getMovieList", methods=['GET'])
def getMovieList():

    movies_count = mongo.db.movie_meta100k.count()
    random_movieId_list = movieRecom.randhomChooseMovies(movies_count)

    movie_query_list = []

    for _movieId in random_movieId_list:
        _movieInfo = mongo.db.movie_meta100k.find_one({'movieId': _movieId})
        movie_query_list.append(_movieInfo)

    print(movie_query_list)


    return dumps(movie_query_list)



"""
below is recommend algo for new user

"""

@app.route("/insertNewUserRating", methods=['POST'])
def insertNewUserRecomMovies():

    # _insertJson = request.get_json()
    # print(_insertJson)

    return Response(status=200, mimetype="application/json")



@app.route("/getNewUserRecomMovies", methods=['POST'])
def getNewUserRecomMovies():
    """
    received new user first rating from "new-user page" from Angular,
    load high-rating movielist and find most similar movie to these movies as recommendation result
    :return: recommend-movielist
    """
    recomMovieList = {}
    recomMovieListbyUserSim = []
    recomMovieListbyMovieSim = []
    try:
        _newUser_rating_json = request.get_json()

        _newUser_rating_dict = _newUser_rating_json['movieRating']

        _newUser_favoriteMovie_list = movieRecom.findUserFavoriteMovies(_newUser_rating_dict)


        ## Recommend movie based on user behavior - find similar user

        _ratingMatrix = movieRecom.getRatingMatrix(_newUser_rating_dict, 1682)
        simUserIdList = movieRecom.newUserFoldinAlgorithm(SVD_users_matrix, SVD_sigma_matrix, SVD_movies_matrix,
                                                          _ratingMatrix, 1682)

        for _userId in simUserIdList:
            _userMoviePreference = mongo.db.user_Top10Movies.find_one({"userId": int(_userId)})
            recomMovieListbyUserSim = recomMovieListbyUserSim + _userMoviePreference["top10Movies"]


        ## Recommmend movie based on user high-rating movie

        _newUser_favoriteMovie_list = movieRecom.findUserFavoriteMovies(_newUser_rating_dict)
        recommend_movieIdlist = []
        for _movieId in _newUser_favoriteMovie_list:
            _movieInfo = mongo.db.movie_Top5Sim100K.find_one({"movieId": int(_movieId)})
            recommend_movieIdlist = recommend_movieIdlist + _movieInfo['movies_cossim']

        for _recom_movieId in recommend_movieIdlist:
            _movieInfo = mongo.db.movie_meta100k.find_one({"movieId": _recom_movieId})
            recomMovieListbyMovieSim.append(_movieInfo)

    except:
        print("New user recommend system failed, send most popular movielist")
        movies_count = mongo.db.movie_meta100k.count()
        random_movieId_list = movieRecom.randhomChooseMovies(movies_count)


        for _movieId in random_movieId_list:
            _movieInfo = mongo.db.movie_meta100k.find_one({'movieId': _movieId})
            recomMovieListbyUserSim.append(_movieInfo)
            recomMovieListbyMovieSim.append(_movieInfo)

    finally:

        recomMovieList["UserSim"] = recomMovieListbyUserSim
        recomMovieList["MovieSim"] = recomMovieListbyMovieSim

        print(recomMovieList)

        return dumps(recomMovieList)


"""
below is the recommend algo for old user
"""
@app.route("/getOldUserRecomMovieList", methods=['POST'])
def getOldUserRecomMovieLists():
    recomMovieList = {}
    recomMovieListbyMovieSim = []
    recomMovieListbyUserSim = []
    try:
        request_json = request.get_json()
        userId = request_json["userId"]
        recomMovieList = {}

        ## recom movie based on similar user preference
        _similarUserId = mongo.db.users_Top5Sim100K.find_one({"userId": userId})

        for _userId in _similarUserId["users_cossim"]:
            _movieIdList = mongo.db.user_Top10Movies.find_one({"userId": _userId})
            recomMovieListbyUserSim = recomMovieListbyUserSim + _movieIdList["top10Movies"]

        ## recom movie based on similar movie preference
        recomMovieIdListbyMovieSim = []
        _userMoviePreference = mongo.db.user_Top10Movies.find_one({"userId": userId})

        for _movieInfo in _userMoviePreference["top10Movies"]:
            _movieIdList = mongo.db.movie_Top5Sim100K.find_one({"movieId": _movieInfo["movieId"]})
            recomMovieIdListbyMovieSim = recomMovieIdListbyMovieSim + _movieIdList["movies_cossim"]

        for _movieId in recomMovieIdListbyMovieSim:
            _movieInfoRecom = mongo.db.movie_meta100k.find_one({"movieId": _movieId})
            recomMovieListbyMovieSim.append(_movieInfoRecom)
    except:
        print("Old user recommend system failed, send most popular movielist")
        movies_count = mongo.db.movie_meta100k.count()
        random_movieId_list = movieRecom.randhomChooseMovies(movies_count)

        for _movieId in random_movieId_list:
            _movieInfo = mongo.db.movie_meta100k.find_one({'movieId': _movieId})
            recomMovieListbyUserSim.append(_movieInfo)
            recomMovieListbyMovieSim.append(_movieInfo)

    finally:
        recomMovieList["UserSim"] = recomMovieListbyUserSim
        recomMovieList["MovieSim"] = recomMovieListbyMovieSim

        print("Old User Rec Success")

        return dumps(recomMovieList)

##############################testing controller#################################
@app.route("/getNewUserRecom", methods=['POST'])
def getNewUserRecom():
    """

    received new user first rating from "new-user page" from Angular,
    load high-rating movielist and find most similar movie to these movies as recommendation result

    :return: recommend-movielist
    """
    _newUser_rating_json = request.get_json()

    _newUser_rating_dict = _newUser_rating_json['movieRating']

    recomMovieList = {}
    recomMovieListbyUserSim = []
    recomMovieListbyMovieSim = []

    try:
        ## Recommend movie based on user behavior - find similar user
        _ratingMatrix = movieRecom.getRatingMatrix(_newUser_rating_dict, 1682)
        simUserIdList = np.array([7, 366,  90, 446, 264])

        for _userId in simUserIdList:
            _userMoviePreference = mongo.db.user_Top10Movies.find_one({"userId": int(_userId)})
            recomMovieListbyUserSim = recomMovieListbyUserSim + _userMoviePreference["top10Movies"]

        print(recomMovieListbyUserSim)

        ## Recommmend movie based on user high-rating movie
        _newUser_favoriteMovie_list = movieRecom.findUserFavoriteMovies(_newUser_rating_dict)
        recommend_movieIdlist = []
        for _movieId in _newUser_favoriteMovie_list:
            _movieInfo = mongo.db.movie_Top5Sim100K.find_one({"movieId": int(_movieId)})
            recommend_movieIdlist = recommend_movieIdlist + _movieInfo['movies_cossim']


        for _recom_movieId in recommend_movieIdlist:
            _movieInfo = mongo.db.movie_meta100k.find_one({"movieId": _recom_movieId})
            recomMovieListbyMovieSim.append(_movieInfo)
    except:
        print("New user recommend system failed, send most popular movielist")
        movies_count = mongo.db.movie_meta100k.count()
        random_movieId_list = movieRecom.randhomChooseMovies(movies_count)

        for _movieId in random_movieId_list:
            _movieInfo = mongo.db.movie_meta100k.find_one({'movieId': _movieId})
            recomMovieListbyUserSim.append(_movieInfo)
            recomMovieListbyMovieSim.append(_movieInfo)
    finally:
        recomMovieList["UserSim"] = recomMovieListbyUserSim
        recomMovieList["MovieSim"] = recomMovieListbyMovieSim

        print("New User Rec Success")

        return dumps(recomMovieList)
##################################################################

if __name__ == "__main__":
    SVD_users_matrix = np.memmap('/project/src/configuration/SVD_user_matrix.dat',
                                        dtype="float32", mode="r", shape=(943, 100))

    SVD_movies_matrix = np.memmap('/project/src/configuration/SVD_movie_matrix.dat',
                                        dtype="float32", mode="r", shape=(100, 1682))

    SVD_sigma_matrix = np.memmap('/project/src/configuration/SVD_sigma_matrix.dat',
                                 dtype="float32", mode='r', shape=(100, 100))
    app.run(host='0.0.0.0', port=5000, debug=True)