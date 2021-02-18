from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_cors import CORS

from bson.json_util import dumps
from flask_pymongo import PyMongo

from flask import Response
import movieRecom
import numpy as np
import pandas as pd
import json
import util


import warnings
warnings.filterwarnings('ignore')

from keras.models import load_model

app = Flask(__name__)
CORS(app) ## cross region 跨域处理
app.config['MONGO_URI'] = "mongodb+srv://root:13820381042bq@recomsys.zqcg8.mongodb.net/PandoRec?retryWrites=true&w=majority"
mongo = PyMongo(app)

### loading Nerual CF Recommendation model
global NeuralCF

### loading MongoDB Collection
global userLogin
global MovieMeta
global UserSimOffline
global UserLikeTop10
global MovieSimOffline
global MovieAvgRate
global MovieRateCount
global Top10MovieEachGenres

global UserIDMapping
global MovieIDMapping
global popularMovieList


def checkNewUserOrNot(user):
    _user_features = UserSimOffline.find_one({'userId': user['userId']})
    if not _user_features:
        #this is new user since there is no user-feature matrix
        return True
    else:
        return False


@app.route("/register", methods=['POST'])
def registerUser():

    _registerUser = request.get_json(force=True)

    print(_registerUser)
    _username = _registerUser['username']
    _password = _registerUser['password']
    _email = _registerUser['email']
    _newId = userLogin.count()+1

    ## First check if user already registered
    _user = userLogin.find_one({'username': _username})
    if not _user:
        _registerUser2DB = {
            "username": _username,
            "password": _password,
            "email": _email,
            "userId": _newId
        }

        ## check if insertion succeed
        _id = userLogin.insert_one(_registerUser2DB)

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
    _user = userLogin.find_one({'username': _loginUser['username']})
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

##################  new user recommend ####################

@app.route("/getMovieList", methods=['GET'])
def getMovieList():

    return dumps(popularMovieList)




################### old user recommend ####################

@app.route("/getOldUserRecomMovieList", methods=['POST'])
def getOldUserRecomMovieLists():
    recomMovieList = {}
    recomMovieListbyMovieSim = []
    recomMovieListbyUserSim = []


    try:
        request_json = request.get_json()
        userId = request_json["userId"]
        userId_inner = UserIDMapping[str(userId)]
        recomMovieList = {}

        ## recom movie based on similar user preference
        recomMovieIdListbyUserSim = []
        _similarUserId = UserSimOffline.find_one({"userId": userId})

        for _userId in _similarUserId["sim_user"]:
            _movieIdList = UserLikeTop10.find_one({"userId": _userId})
            recomMovieIdListbyUserSim = recomMovieIdListbyUserSim + _movieIdList["like_top10"]

        for _movieId in recomMovieIdListbyUserSim[:10]:
            _movieInfoRecom = MovieMeta.find_one({"movieId": _movieId})
            _movieInfoRecom["AvgRate"] = MovieAvgRate.find_one({"movieId": _movieId})['avg_rate']
            _movieInfoRecom["RateCount"] = MovieRateCount.find_one({"movieId": _movieId})['count']

            ## Predict rating value
            _movieId_inner = MovieIDMapping[str(_movieId)]
            _movieInfoRecom['PredRate'] = round(
                float(NeuralCF.predict([pd.Series([userId_inner]), pd.Series([_movieId_inner])])[0][0]), 2
            )


            recomMovieListbyUserSim.append(_movieInfoRecom)

        ## recom movie based on similar movie preference
        recomMovieIdListbyMovieSim = []
        _userMoviePreference = UserLikeTop10.find_one({"userId": userId})

        for _movieInfo in _userMoviePreference["like_top10"]:
            _movieIdList = MovieSimOffline.find_one({"movieId": _movieInfo})
            recomMovieIdListbyMovieSim = recomMovieIdListbyMovieSim + _movieIdList["sim_movie"]

        for _movieId in recomMovieIdListbyMovieSim[:10]:
            _movieInfoRecom = MovieMeta.find_one({"movieId": _movieId})
            _movieInfoRecom["AvgRate"] = MovieAvgRate.find_one({"movieId": _movieId})['avg_rate']
            _movieInfoRecom["RateCount"] = MovieRateCount.find_one({"movieId": _movieId})['count']

            ## Predict rating value
            _movieId_inner = MovieIDMapping[str(_movieId)]
            _movieInfoRecom['PredRate'] = round(
                float(NeuralCF.predict([pd.Series([userId_inner]), pd.Series([_movieId_inner])])[0][0]), 2
            )

            recomMovieListbyMovieSim.append(_movieInfoRecom)
        print("Old User Rec Success")
    except:
        print("Old user recommend system failed, send most popular movielist")
        movies_count = MovieMeta.count()
        random_movieId_list = movieRecom.randhomChooseMovies(movies_count)

        for _movieId in random_movieId_list:
            _movieInfoRecom = MovieMeta.find_one({'movieId': _movieId})
            _movieInfoRecom["AvgRate"] = MovieAvgRate.find_one({"movieId": _movieId})['avg_rate']
            _movieInfoRecom["RateCount"] = MovieRateCount.find_one({"movieId": _movieId})['count']

            ## Predict rating value
            _movieId_inner = MovieIDMapping[str(_movieId)]
            _movieInfoRecom['PredRate'] = round(
                float(NeuralCF.predict([pd.Series([userId_inner]), pd.Series([_movieId_inner])])[0][0]), 2
            )

            recomMovieListbyUserSim.append(_movieInfoRecom)
            recomMovieListbyMovieSim.append(_movieInfoRecom)

    finally:
        recomMovieList["UserSim"] = recomMovieListbyUserSim
        recomMovieList["MovieSim"] = recomMovieListbyMovieSim
        print(recomMovieList)


        return dumps(recomMovieList)




if __name__ == "__main__":

    NeuralCF = load_model('../neural_cf')

    with open('../user_id_map.json', 'r') as f:
        UserIDMapping = json.load(f)
    f.close()

    with open('../movie_id_map.json', 'r') as f:
        MovieIDMapping = json.load(f)
    f.close()

    with open('../popular_movielist.json', 'r') as f:
        popularMovieList = json.load(f)
    f.close()


    userLogin = mongo.db.UserInfo
    MovieMeta = mongo.db.MovieMeta
    UserSimOffline = mongo.db.UserSimOffline
    UserLikeTop10 = mongo.db.UserLikeTop10
    MovieSimOffline = mongo.db.MovieSimOffline
    MovieAvgRate = mongo.db.MovieAvgRate
    MovieRateCount = mongo.db.MovieRateCnt
    Top10MovieEachGenres = mongo.db.Top10MovieEachGenres

    app.run(debug=True)