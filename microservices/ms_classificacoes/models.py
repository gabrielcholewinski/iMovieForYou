from datetime import datetime
from config import db, ma
from flask_marshmallow import Marshmallow, fields

# Classifications : movie-id, average_rating, num_ratings
# tabela2 : user_id, movie_id, rating

class Classification(db.Model):
    __tablename__ = 'classification'
    tconst = db.Column(db.Integer, primary_key=True)
    averageRating = db.Column(db.Float)
    numVotes = db.Column(db.Integer)

class UserRating(db.Model):
    __tablename__ = 'userRating'
    user_id = db.Column(db.Integer, primary_key=True)
    tconst = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)

class ClassificationsSchema(ma.Schema):
    class Meta:
        model = Classification
        sqla_session = db.session


class UserRatingSchema(ma.Schema):
    class Meta:
        model = UserRating
        sqla_session = db.session


