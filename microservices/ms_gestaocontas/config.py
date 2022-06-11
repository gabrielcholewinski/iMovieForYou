import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Google Cloud SQL (change this accordingly)
PASSWORD ="*****"
PUBLIC_IP_ADDRESS ="**.***.***.**"
DBNAME ="************"
PROJECT_ID ="*******"
INSTANCE_NAME ="*******"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+mysqlconnector://{0}:{1}@{2}/{3}".format(
        "root", 
        PASSWORD,
        PUBLIC_IP_ADDRESS, DBNAME
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance -> make models for database ORM for us -> see part2 realpython
db = SQLAlchemy(app)

# Initialize Marshmallow -> serialize / deserialize in JSON for us -> see part2 realpython
ma = Marshmallow(app)
