from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_cors import CORS

from bson.json_util import dumps
from flask_pymongo import PyMongo

from flask import Response
import movieRecom
import numpy as np


app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://root:13820381042bq@recomsys.zqcg8.mongodb.net/LearnMongo?retryWrites=true&w=majority"
mongo = PyMongo(app)
global SVD_users_matrix
global SVD_movies_matrix



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
    _user_features = mongo.db.user_features100K.find_one({'userId': user['userId']})
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

@app.route("/getRecomMovies", methods=['POST'])
def getRecomMovies():
    recomMovieList = [
        {
            "movie": "Toy Story",
            "release": "2000"
        },
        {
            "movie": "Star War",
            "release": "2001"
        },
    ]

    return jsonify(recomMovieList)


@app.route("/insertNewUserRating", methods=['POST'])
def insertNewUserRecomMovies():

    _insertJson = request.get_json()
    print(_insertJson)

    return Response(status=203, mimetype="application/json")


@app.route("/getNewUserRecomMovies", methods=['POST'])
def getNewUserRecomMovies():
    pass

if __name__ == "__main__":
    SVD_users_matrix=np.memmap('D:/CapstonePJ/NetflixRecom/recom-restapi/configuration/SVD_user_matrix.dat',
                                        dtype="float32", mode="r", shape=(943, 100))

    SVD_movies_matrix=np.memmap('D:/CapstonePJ/NetflixRecom/recom-restapi/configuration/SVD_movie_matrix.dat',
                                        dtype="float32", mode="r", shape=(100, 1682))
    app.run(debug=True)