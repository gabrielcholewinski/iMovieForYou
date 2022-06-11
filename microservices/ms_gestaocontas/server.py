"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, make_response
import connexion
import json

# Create the application instance
app = connexion.App(__name__, specification_dir="swagger-api-trabalho/")

# read the swagger.yml file to configure the endpoints
# app.add_api("swagger.yml")

# read the auth swagger.yml file to configure the endpoints
app.add_api("swagger-sa-auth.yml")

port=5003

# Create a URL route in our application for "/"
@app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5003/

    :return:        the rendered template "home.html"
    """
    data = make_response(json.dumps({"return": "OK"}))
    data.status_code = 200
    return data


if __name__ == "__main__":
    app.run(port=5003,debug=True)
