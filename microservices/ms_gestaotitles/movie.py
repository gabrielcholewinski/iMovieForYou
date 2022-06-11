"""
This is the movie module and supports all the ReST actions for the
MOVIE collection
"""
import sys

from flask import abort, make_response

from config import db, app
from models import Movie, MovieSchema, Title, Movie_Genre, Genre, Rating

def create(movie):
    """
    This function creates a new movie in the movie structure
    based on the passed in title data
    :param movie:  movie to create in movie structure
    :return:        201 on success, 406 on movie exists
    """

    title_maintype = movie.get("titleType")
    title_name = movie.get("primaryTitle")
    title_genre = movie.get("movie_genre")
    title_startyear = movie.get("startYear")
    title_runtime = movie.get("runTime")
    title_isadult = movie.get("isAdult") 
    title_endyear = movie.get("endYear") 
    title_titles = movie.get("titles")

    # title_genre_genre = title_genre
    # 
#        .filter(Movie.genre == title_genre) \
    existing_movie = Movie.query.filter(Movie.primaryTitle == title_name) \
        .filter(Movie.startYear == title_startyear) \
        .filter(Movie.titleType == title_maintype) \
        .filter(Movie.runTime == title_runtime) \
        .filter(Movie.isAdult == title_isadult) \
        .one_or_none()

    # Can we insert this movie?
    if existing_movie is None:

        movieschema = MovieSchema()

        # print(movie, file=sys.stderr)
        # new_movie = movieschema.load(movie, session=db.session)

        existing_genre_list = []
        for genero in title_genre:
            existing_genre = Genre.query.filter(Genre.genre_name == genero.get("genre").get("genre_name")).one_or_none()
            if existing_genre is not None:
                existing_genre_list.append(existing_genre)
            else:
                # new_genre = Genre(genre_name=genero.genre.genre_name)
                # existing_genre_list.append(new_genre)
                abort(
                    400,
                    "Genre {genero} does exists. Must use one of the generes given: "
                    "[Documentary,Short,Animation,Comedy,Romance,Sport,Action,News,Drama,Fantasy,Horror,Biography,Music,War,Crime,Western,Family,Adventure,History,Mystery,Sci-Fi,Thriller,Musical,Film-Noir,Game-Show,Talk-Show,Reality-TV,Adult]".format(
                        genero=genero.get("genre").get("genre_name"),
                    ),)

        new_movie = Movie(titleType=title_maintype, primaryTitle=title_name, isAdult=title_isadult, startYear=title_startyear,
        endYear=title_endyear,runTime=title_runtime)

        new_rating = Rating(averageRating=movie.get("rating").get("averageRating"), numVotes=movie.get("rating").get("numVotes"))
        new_movie.rating = new_rating

        new_title_list = []
        for title in title_titles:
            new_title = Title(ordering=title.get("ordering"),title=title.get("title"),
            region=title.get("region"),language=title.get("language"))
            new_title_list.append(new_title)
        new_movie.titles = new_title_list

        new_movie_genre_list = []

        for g in existing_genre_list:
            new_movie_genre = Movie_Genre(genre_id=g.genre_id,genre=g)
            new_movie_genre_list.append(new_movie_genre)
        new_movie.movie_genre = new_movie_genre_list
        
        # Add the movie to the database
        db.session.add(new_movie)
        db.session.commit()

        # Serialize and return the newly created movie in the response
        data = movieschema.dump(new_movie)

        return data, 201

    # Otherwise, nope, movie exists already
    else:
        abort(
            409,
            "Movie {title_name} exists already".format(
                title_name=title_name,
            ),
        )


@app.route('/movies/<int:title_id>', methods=['DELETE'])
def delete(title_id):
    """
    This function deletes a movie from the movie structure
    :param title_id:   Id of the movie to delete
    :return:            200 on successful delete, 404 if not found
    """
    movie = Movie.query.filter(Movie.tconst == title_id).one_or_none()
    if movie is not None:
        db.session.delete(movie)
        db.session.commit()
        return make_response(
            "Movie {title_id} deleted".format(title_id=title_id), 200
        )

    # Otherwise, nope, didn't find that movie
    else:
        abort(
            404,
            "Movie not found for Id: {title_id}".format(title_id=title_id),
        )


def read_all():
    """
    This function responds to a request for /api/movies
    with the complete lists of movies
    :return:        json string of list of movies
    """
    # Create the list of movie from our data
    # mudado para primary title
    try:
        movie = Movie.query.order_by(Movie.primaryTitle).limit(20).all()
        # Serialize the data for the response
        movie_schema = MovieSchema(many=True)
        data = movie_schema.dump(movie)
        return data
    except:
        db.rollback()
        abort(404, "Rollback Error")



def read_one(title_id):
    """
    This function responds to a request for /movies/{title_id}

    :param title_id: title_id of the movie will be compared to tconst
    :return:        movie
    """
    try:
        movie = Movie.query.filter(Movie.tconst == int(title_id)).one_or_none()
        if movie is not None:
            movie_schema = MovieSchema()
            return movie_schema.dump(movie)

        else:
            abort(404, f"Movie not found for Id: {title_id}")
    except:
        db.rollback()
        abort(404, "Rollback Error")


def read_filtered(primaryTitle, genre, region, language, startYear):
    """
    This function responds to a request for movies/filtered?primaryTitle=&&genre=&&region=&&language=&&startYear=

    :param:         search filters (title, genre, region, language and startYear)
    :return:        movieList
    """
    try:
        # Build the initial query 
        query = Movie.query.join(Title).join(Movie_Genre).join(Genre)

        if primaryTitle:
            query = query.filter(Movie.primaryTitle == primaryTitle)
        if region:
            query = query.filter(Title.region == region)
        if language:
            query = query.filter(Title.language == language)
        if startYear:
            query = query.filter(Movie.startYear == startYear)
        if genre:
            query = query.filter(Genre.genre_name == genre) 

        movieList = query.limit(30).all()

        movielistComp = []
        if movieList is not None:
            # Serialize the data for the response
            movie_schema = MovieSchema(many=True)
            data = movie_schema.dump(movieList)
            return data

        else:
            abort(404, f"Movie not found for Filters")
    except:
        db.rollback()
        abort(404, "Rollback Error")
