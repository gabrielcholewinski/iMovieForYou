import os
from config import db
from models import Movie, Title, Rating, Movie_Genre, Genre

# Data to initialize database with
MOVIES = [
    {"tconst": 1,
     "titleType": "short",
     "primaryTitle": "Carmencita",
     "isAdult": 0,
     "startYear": "1894",
     "endYear": "",
     "runTime": 1
    #  "genre": "Documentary,Short"
     },

    {"tconst": 2,
     "titleType": "short",
     "primaryTitle": "Le clown et ses chiens",
     "isAdult": 0,
     "startYear": "1892",
     "endYear": "",
     "runTime": 5
    #  "genre": "Animation,Short"
     },

    {"tconst": 3,
     "titleType": "short",
     "primaryTitle": "Pauvre Pierrot",
     "isAdult": 0,
     "startYear": "1892",
     "endYear": "",
     "runTime": 4
    #  "genre": "Animation,Comedy,Romance"
     }
]

TITLES = [
    {"titleId": 1,
     "ordering": 1,
     "title": "Carmencita - spanyol tánc",
     "region": "HU",
     "language": "sv"
     },

    {"titleId": 1,
     "ordering": 2,
     "title": "Καρμενσίτα",
     "region": "GR",
     "language": ""
     },

    {"titleId": 2,
     "ordering": 1,
     "title": "Le clown et ses chiens",
     "region": "FR",
     "language": "fr"
     },

    {"titleId": 2,
     "ordering": 2,
     "title": "The Clown and His Dogs",
     "region": "US",
     "language": "en"
     },

    {"titleId": 3,
     "ordering": 1,
     "title": "Poor Pierrot",
     "region": "GB",
     "language": "en"
     }
]

RATINGS = [
    {"tconst": 1,
     "averageRating": 5.6,
     "numVotes": 1550
     },

    {"tconst": 2,
     "averageRating": 6.1,
     "numVotes": 186
     },

    {"tconst": 3,
     "averageRating": 6.5,
     "numVotes": 1207
     }
]

MOVIE_GENRE = [
    {"tconst": 1,
    "genre_id": 1
    },
    {"tconst": 1,
    "genre_id": 2
    },
    {"tconst": 2,
    "genre_id": 3
    },
    {"tconst": 2,
    "genre_id": 2
    },
    {"tconst": 3,
    "genre_id": 3
    },
    {"tconst": 3,
    "genre_id": 4
    },
    {"tconst": 3,
    "genre_id": 5
    }
]


GENRE = [
    {"genre_id" : 1,
    "genre_name": "Documentary"
    },

    {"genre_id" : 2,
    "genre_name": "Short"
    },

    {"genre_id" : 3,
    "genre_name": "Animation"
    },

    {"genre_id" : 4,
    "genre_name": "Comedy"
    },

    {"genre_id" : 5,
    "genre_name": "Romance"
    }
]

# Delete database file if it exists currently
if os.path.exists("gestaofilmes.db"):
    os.remove("gestaofilmes.db")

# Create the database
db.create_all()

# iterate over the MOVIE structure and populate the database
for movie in MOVIES:
    m = Movie(tconst=movie.get("tconst"),
              titleType=movie.get("titleType"),
              primaryTitle=movie.get("primaryTitle"),
              isAdult=movie.get("isAdult"),
              startYear=movie.get("startYear"),
              endYear=movie.get("endYear"),
              runTime=movie.get("runTime"))
            #   genre=movie.get("genre"))

    db.session.add(m)

db.session.commit()

# iterate over the TITLES structure and populate the database
for title in TITLES:
    t = Title(titleId=title.get("titleId"),
              ordering=title.get("ordering"),
              title=title.get("title"),
              region=title.get("region"),
              language=title.get("language"))

    db.session.add(t)

db.session.commit()

# iterate over the RATINGS structure and populate the database
for rating in RATINGS:
    r = Rating(tconst=rating.get("tconst"),
               averageRating=rating.get("averageRating"),
               numVotes=rating.get("numVotes"))

    db.session.add(r)

db.session.commit()

for movie_genre in MOVIE_GENRE:
    mg = Movie_Genre(tconst=movie_genre.get("tconst"),
               genre_id=movie_genre.get("genre_id"))

    db.session.add(mg)

db.session.commit()

for genre in GENRE:
    g = Genre(genre_id=genre.get("tconst"),
               genre_name=genre.get("genre_name"))

    db.session.add(g)

db.session.commit()
