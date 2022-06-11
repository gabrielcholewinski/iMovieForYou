import os
from config import db
from models import Classification, UserRating

# Data to initialize database with
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
#CONFIRMAR O RANGE DO RATING E FLOATS AND STUFF
USERRATING = [
    {
        'user_id': '1',
        'tconst': '1',
        'rating': '5.6',
        
    },
    {
        'user_id': '2',
        'tconst': '2',
        'rating': '7.6',
    },
    {
        'user_id': '3',
        'tconst': '3',
        'rating': '5.9',
    }
]
#Delete database file if it exists currently
if os.path.exists("classifications.db"):
    os.remove("classifications.db")

# Create the database
db.create_all()

# Iterate over the PEOPLE structure and populate the database
for classification in RATINGS:
    c = Classification(tconst=classification.get("tconst"), averageRating=classification.get("averageRating"), numVotes=classification.get("numVotes"))

    db.session.add(c)

for userrating in USERRATING:
    ur = UserRating(user_id=userrating.get("user_id"), tconst=userrating.get("tconst"), rating=userrating.get("rating"))

    db.session.add(ur)

db.session.commit()