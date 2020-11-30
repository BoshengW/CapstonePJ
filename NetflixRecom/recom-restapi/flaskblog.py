from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_cors import CORS

from bson.json_util import dumps
from util import load_movie_question
from flask_pymongo import PyMongo

from flask import Response


app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://root:13820381042bq@recomsys.zqcg8.mongodb.net/LearnMongo?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/register", methods=['POST'])
def regusterUser():

    _registerUser = request.get_json(force=True)

    print(_registerUser)
    _username = _registerUser['username']
    _password = _registerUser['password']
    _email = _registerUser['email']
    _newId = mongo.db.learnInsert.count()+1

    ## First check if user already registered
    _user = mongo.db.learnInsert.find_one({'username': _username})
    if not _user:
        _registerUser2DB = {
            "username": _username,
            "password": _password,
            "email": _email,
            "userId": _newId
        }

        ## check if insertion succeed
        _id = mongo.db.learnInsert.insert_one(_registerUser2DB)

        if not _id:
            return Response(status=203, mimetype="application/json")
        else:
            return Response(status=200, mimetype="application/json")
    else:
        return Response(status=203, mimetype="application/json")




@app.route("/loginInfo", methods=['GET', 'POST'])
def validateUserInfo():

    _loginUser = request.get_json(force=True)
    print(_loginUser)
    _username = _loginUser['username']
    _password = _loginUser['password']
    # add username and password back to frontend- not recommand
    _user = mongo.db.learnInsert.find_one({'username': _username})

    print(_user)
    resp = dumps(_user)

    return resp

@app.route("/getMovieList", methods=['GET'])
def getMovieList():
    movieList = load_movie_question('configuration/movie_questions.json')
    print(movieList)

    return jsonify(movieList)

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


if __name__ == "__main__":
    app.run(debug=True)