import time
import google
import requests
from google.auth import jwt
from google.auth import crypt


# Autenticação
# Funções para fazer a token JWT
# Ver Audience


def generate_jwt(sa_keyfile,
                 sa_email='unified-sa-authorization@cnprojext.iam.gserviceaccount.com',
                 audience='your-service-name',
                 expiry_length=3600):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        # expires after 'expiry_length' seconds.
        "exp": now + expiry_length,
        # iss must match 'issuer' in the security configuration in your
        # swagger spec (e.g. service account email). It can be any string.
        'iss': sa_email,
        # aud must be either your Endpoints service name, or match the value
        # specified as the 'x-google-audience' in the OpenAPI document.
        'aud': audience,
        # sub and email should match the service account's email address
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)

    return jwt


def make_jwt_request(signed_jwt, url='https://your-endpoint.com'):
    """Makes an authorized request to the endpoint"""
    headers = {
        'Authorization': 'Bearer {}'.format(signed_jwt.decode('utf-8')),
        'content-type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print(response.status_code, response.content)
    response.raise_for_status()


def parseMovie(movie):
    movieFile = []
    movieFile.append(movie.tconst)
    movieFile.append(movie.titleType)
    movieFile.append(movie.primaryTitle)
    movieFile.append(movie.startYear)
    movieFile.append(movie.endYear)
    movieFile.append(movie.runTime)
    movieFile.append(movie.isAdult)
    movieFile.append(movie.genre)
    titles = []
    for t in movie.titles:
        titles.append(t.ordering),
        titles.append(t.title),
        titles.append(t.region),
        titles.append(t.language)
    movieFile.append(titles)
    rating = []
    for r in movie.rating:
        rating.append(r.averageRating),
        rating.append(r.numVotes)
    movieFile.append(rating)
    casts = []
    for c in movie.casts:
        casts.append(c.ordering),
        casts.append(c.category),
        casts.append(c.characters),
        casts.append(c.nconst)
        casts.append(c.name.primaryName),
        casts.append(c.name.birthYear),
        casts.append(c.name.deathYear)
    movieFile.append(casts)
    return movieFile
