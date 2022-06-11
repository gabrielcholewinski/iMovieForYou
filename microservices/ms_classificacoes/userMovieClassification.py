"""
This is the watchMovies module and supports all the ReST actions for the
watchedMovies collection
"""

import requests
from flask import Flask, abort, make_response

from config import db
from utilitarios_classificacao import generate_jwt, make_jwt_request
from models import UserRating, Classification
import json

app = Flask(__name__)


@app.route('/user/<int:user_id>/rating/<int:movie_id>', methods=["POST"])
def addRatingToMovie(user_id, movie_id, rating):
    """
    This function responds to a request for /user/{userId}/userMovieList
    with one matching user from users

    :param user_id:  user_id of person to find
    :return:        moviesList matching userId moviesList
    """
    try:
        # Starts with Authentication Part: Must have the key to use
        # Key is local, this is insecure, but for development it is okay
        # Need to see if the key format is right. It should be, it is from tutorial directly
        sa_keyfile = open("unified-sa-authorization-keys.json", "r")
        my_temp_jwt = generate_jwt(sa_keyfile, audience="http://imoviesforyou.me/classificacoes")
        sa_keyfile.close()

        request_url = 'http://34.120.57.34/gestaocontas/user/' + str(user_id) + '/userMovieList'
        resp = make_jwt_request(my_temp_jwt, request_url)

        # old resp, if needed to check anything, just comment the above and uncomment below one
        # resp = requests.get('http://34.120.57.34/gestaocontas/user/' + str(user_id) + '/userMovieList')
        if resp.status_code != 200:
            abort(404, "User does not exists")

        r = json.loads(resp.content.decode())

        if movie_id not in r.get("movieList"):
            abort(404, "User has not seen the movie with id = " + str(movie_id))

        movieRate = Classification.query.filter(Classification.tconst == movie_id).one_or_none()

        if movieRate is None:
            abort(404, "Movie does not exists")

        # Build the initial query
        userRating = (
            UserRating.query.filter(UserRating.user_id == user_id).filter(UserRating.tconst == movie_id).one_or_none()
        )

        if userRating is None:

            x = float(rating)

            n = movieRate.numVotes + 1
            avg = (movieRate.averageRating + x) / 2

            Classification.query.filter(Classification.tconst == movie_id).update(
                {Classification.averageRating: avg, Classification.numVotes: n})

            new_rating = UserRating(user_id=user_id, tconst=movie_id, rating=x)

            db.session.add(new_rating)
            db.session.commit()

            rating = {"userRating": [new_rating.user_id, new_rating.tconst, new_rating.rating]}
            data = make_response(json.dumps(rating))
            data.status_code = 201
            return data
        else:
            abort(409, f"Rating already added")
    except:
        db.rollback()
        abort(404, "Rollback Error")

