"""
This is the watchMovies module and supports all the ReST actions for the
watchedMovies collection
"""
from flask import Flask, abort, make_response
from config import db
from microservices.ms_gestaocontas.utilitarios_gestaocontas import generate_jwt, make_jwt_request
from models import User, UserMovieListSchema, UserSchema, UserMoviesList
from build_database import USERS
from sqlalchemy import insert
import requests
import json

app = Flask(__name__)

@app.route('/user/<int:user_id>/userMovieList', methods=["GET"])
def getMovieUserList(user_id):
    """
    This function responds to a request for /user/{userId}/userMovieList
    with one matching user from users

    :param userId:  userId of person to find
    :return:        moviesList matching userId moviesList
    """
    try:
        # Build the initial query
        userMoviesList = UserMoviesList.query.filter(UserMoviesList.user_id == user_id).all()
        
        movielist = []
        if userMoviesList is not None:
            for row in userMoviesList:
                movielist.append(row.movie)
            x = {"movieList": movielist}
            data = make_response(json.dumps(x))
            return data
            
        else:
        abort(404, f"User not found for Id: {user_id}")
        
    except:
        db.rollback()
        abort(404, "Rollback Error")

@app.route('/user/<int:user_id>/userMovieList', methods=["POST"])
def addMovieToUserList(user_id, movie):
    """
    This function adds a new movie to the user movies list

    :param userId:  user where a movie is going to be added to it's list
    :param movie:   movie to be added in user list
    :return:        201 on success, 406 on person exists
    """
    try:
        user = User.query.filter(User.user_id == user_id).one_or_none()

        if user is None:
            abort(404, f"User not found for Id: {user_id}")

        userMovie = (
            UserMoviesList.query.filter(UserMoviesList.user_id == user_id)
            .filter(UserMoviesList.movie == movie.get("movie")).one_or_none()
        )

        # Starts with Authentication Part: Must have the key to use
        # Key is local, this is insecure, but for development it is okay
        # Need to see if the key format is right. It should be, it is from tutorial directly
        sa_keyfile = open("unified-sa-authorization-keys.json", "r")
        my_temp_jwt = generate_jwt(sa_keyfile, audience="http://imoviesforyou.me/gestaocontas")
        sa_keyfile.close()

        request_url = 'http://34.120.57.34/gestaotitles/movies/'+str(movie.get("movie"))
        resp = make_jwt_request(my_temp_jwt, request_url)

        # old resp, if needed to check anything, just comment the above and uncomment below one
        # resp = requests.get('http://34.120.57.34/gestaotitles/movies/'+str(movie.get("movie")))

        if resp.status_code != 200:
            abort(404, "Movie does not exists")

        if userMovie is None:

            new_movie = UserMoviesList(user_id=user_id,movie=movie.get("movie"))

            db.session.add(new_movie)
            db.session.commit()

            # data = schema.dump(new_movie).data
            movielist = {"userMovie": [new_movie.user_id, new_movie.movie]}
            data = make_response(json.dumps(movielist))
            data.status_code = 201
            return data
        else:
            abort(409, f"Movie already added")
    except:
        db.rollback()
        abort(404, "Rollback Error")