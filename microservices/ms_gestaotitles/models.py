from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from config import db


# This class defines movies
class Movie(db.Model):
    __tablename__ = "title_basics_csv"
    tconst = db.Column(db.Integer, primary_key=True)
    titleType = db.Column(db.String(100))
    primaryTitle = db.Column(db.String(100))
    # genre of title, like horror, comedy, romance
    isAdult = db.Column(db.Integer)  # alterar tipo para boolean 0 ou 1: ok?
    # start year title ran (for series, for example)
    startYear = db.Column(db.String(4))  # YYYY eg 1990
    # end year title ran (for series, for example)
    endYear = db.Column(db.String(4))  # YYYY eg 1990
    # time, in minutes, of the duration of the title (episode in case series)
    runTime = db.Column(db.Integer)  # alterar tipo integer
    # genre = db.Column(db.String(32))  # alterar para ser lista:
    titles = db.relationship('Title', cascade="all, delete", backref='title_basics_csv', lazy='dynamic')
    rating = db.relationship('Rating', cascade="all, delete", uselist=False, backref='title_basics_csv', lazy=False)
    movie_genre = db.relationship('Movie_Genre', cascade="all, delete", backref='title_basics_csv', lazy=False)

# This class defines list of Titles that a movie have
class Title(db.Model):
    __tablename__ = "title_akas_csv"
    titleId = db.Column(db.Integer, db.ForeignKey('title_basics_csv.tconst'), primary_key=True)
    ordering = db.Column(db.Integer, primary_key=True)
    # english title name (to be simplified, just the english title)
    title = db.Column(db.String(300))
    # original region of title (e,g. china, us, brazil,...)
    region = db.Column(db.String(32))
    # original language title (english, portuguese, french, ...)
    language = db.Column(db.String(32))


# This class defines a rating that a movie have
class Rating(db.Model):
    __tablename__ = "title_ratings_csv"
    tconst = db.Column(db.Integer, db.ForeignKey('title_basics_csv.tconst'), primary_key=True)
    averageRating = db.Column(db.Float)
    numVotes = db.Column(db.Integer)


class Movie_Genre(db.Model):
    __tablename__ = "movie_genre_csv"
    tconst = db.Column(db.Integer, db.ForeignKey('title_basics_csv.tconst'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre_csv.genre_id'), primary_key=True)
    genre = db.relationship('Genre', backref='movie_genre_csv', lazy=False)

 # genre of title, like horror, comedy, romance
class Genre(db.Model):
    __tablename__ = "genre_csv"
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(300))
    genre = db.relationship('Movie_Genre', cascade="all, delete", backref='genre_csv', lazy='dynamic')
   

class MovieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        include_relationships = True
        load_instance = True
        sqla_session = db.session
        # exclude = ("tconst",)
    # ver se essse default "" nao explode
    rating = fields.Nested("RatingSchema", default="", many=False)
    titles = fields.Nested("TitleSchema", default=[], many=True)
    movie_genre = fields.Nested("MovieGenreSchema", default="", many=True)


class TitleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Title
        # pode ser necessario voltar com isso depois por causa de preencher as relationships
        # include_relationships = True
        # exclude = ("titleId",)
        load_instance = True
        sqla_session = db.session

class RatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        # include_relationships = True
        # exclude = ("tconst",)
        load_instance = True
        sqla_session = db.session


class MovieGenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie_Genre
        load_instance = True
        sqla_session = db.session
    genre = fields.Nested('GenreSchema', many=False)

class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        sqla_session = db.session