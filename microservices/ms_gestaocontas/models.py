from datetime import datetime
import os
from config import db, ma
from flask_marshmallow import Marshmallow, fields

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), index=True)
    fname = db.Column(db.String(32))
    username = db.Column(db.String(32))
    password = db.Column(db.String(32))
    moviesList = db.relationship(
        'UserMoviesList',
        backref='user',
        cascade='all, delete, delete-orphan',
        single_parent=True
    )

class UserMoviesList(db.Model):
    __tablename__ = 'userMoviesList'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    movie = db.Column(db.Integer, primary_key=True)
    #movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

'''class Movie(db.Model):
    __tablename__ = "movies"
    movie_id = db.Column(db.Integer, primary_key=True)
    # english title name (to be simplified, just the english title)
    movie_name = db.Column(db.String(64))
    # original region of title (e,g. china, us, brazil,...)
    movie_region = db.Column(db.String(32))
    # original language title (english, portuguese, french, ...)
    movie_language = db.Column(db.String(32))
    # start year title ran (for series, for example)
    movie_startYear = db.Column(db.String(4))  # YYYY eg 1990
    # end year title ran (for series, for example)
    movie_endYear = db.Column(db.String(4))  # YYYY eg 1990
    # time, in minutes, of the duration of the title (episode in case series)
    movie_runTime = db.Column(db.Integer)  # alterar tipo integer
    # type of title, like series, movie, short, tvepisode, etc
    movie_mainType = db.Column(db.String(32))
    # genre of title, like horror, comedy, romance
    # title_genres = db.Column(db.String(32))  # alterar para ser lista:
    # genre of title, like horror, comedy, romance
    movie_isAdult = db.Column(db.Boolean)  # alterar tipo para boolean 0 ou 1: ok?'''

class UserSchema(ma.Schema):
    class Meta:
        model = User
        sqla_session = db.session
    moviesList = ma.Nested('UserMovieSchema', default=[], many=True)

class UserMovieSchema(ma.Schema):
    fields = ('user_id', 'movie')

class UserMovieListSchema(ma.Schema):
    class Meta:
        model = UserMoviesList
        sqla_session = db.session
    user = ma.Nested('MovieUserSchema', default=None)

class MovieUserSchema(ma.Schema):
    fields = ('user_id', 'lname', 'fname', 'username', 'password')

'''class MovieSchema(ma.UserSchema):
    class Meta:
        model = User
        sqla_session = db.session'''