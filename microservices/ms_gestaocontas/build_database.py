import os
from config import db
from models import User, UserMoviesList

# Data to initialize database with
USERS = [
    {
        'lname': 'Cholewinski',
        'fname': 'Gabriel',
        'username': 'gabriel_teste',
        'password': '123',
        'moviesList': []
    },
    {
        'lname': 'Ye',
        'fname': 'Joao',
        'username': 'joao_teste',
        'password': '123',
        'moviesList': []
    },
    {
        'lname': 'Koch',
        'fname': 'Raul',
        'username': 'raul_teste',
        'password': '123',
        'moviesList': []
    }
]

'''MOVIES = [

    {
        "movie_name": "Olympians", "title_region": "Greece",
        "movie_language": "greek",
        "movie_startYear": "1000", "title_endYear": "1200",
        "movie_runTime": 23,
        "movie_mainType": "series",
        "movie_isAdult": True
    },

    {
        "movie_name": "Doug", "title_region": "united states",
        "movie_language": "english",
        "movie_startYear": "1994", "title_endYear": "1998",
        "movie_runTime": 20,
        "movie_mainType": "series",
        "movie_isAdult": False
    },
    {
        "movie_name": "Boss 2", "title_region": "united states",
        "movie_language": "english",
        "movie_startYear": "1988", "title_endYear": "1988",
        "movie_runTime": 168,
        "movie_mainType": "movie",
        "movie_isAdult": True
    },
]'''

#Delete database file if it exists currently
if os.path.exists("users.db"):
    os.remove("users.db")

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for user in USERS:
    u = User(lname=user.get("lname"), fname=user.get("fname"), username=user.get("username"), password=user.get("password"))

    # Add the notes for the person
    for uml in user.get("moviesList"):
        movie = uml
        u.moviesList.append(
            UserMoviesList(
                movie=movie
            )
        )
    db.session.add(u)

db.session.commit()