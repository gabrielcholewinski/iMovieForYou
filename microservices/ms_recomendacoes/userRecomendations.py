"""
This is the watchMovies module and supports all the ReST actions for the
watchedMovies collection
"""
import requests
from flask import Flask, abort, make_response

import json

from microservices.ms_recomendacoes.utilitarios_recomendacoes import generate_jwt, make_jwt_request

app = Flask(__name__)


# NECESSARIO ACRESCENTAR MAIS FILMES PARA OS TESTES FUNCIONAREM BEM

@app.route('/user/<int:user_id>/recommended', methods=["GET"])
def read_recommended(user_id):
    """
    This function responds to a request for /user/{userId}/userMovieList
    with one matching user from users

    :param user_id:  user_id of person to find
    :return:        moviesList matching userId moviesList
    """
    # lista corrente de titulos ja vistos pelo user user_id
    jaVistos = []

    # Starts with Authentication Part: Must have the key to use
    # Key is local, this is insecure, but for development it is okay
    # Need to see if the key format is right. It should be, it is from tutorial directly
    sa_keyfile = open("unified-sa-authorization-keys.json", "r")
    my_temp_jwt = generate_jwt(sa_keyfile, audience="http://imoviesforyou.me/recomendacoes")
    sa_keyfile.close()

    request_url = 'http://34.120.57.34/gestaocontas/user/' + str(user_id) + '/userMovieList'
    resp = make_jwt_request(my_temp_jwt, request_url)

    # old resp, if needed to check anything, just comment the above and uncomment below one
    # resp = requests.get('http://34.120.57.34/gestaocontas/user/' + str(user_id) + '/userMovieList')
    if resp.status_code != 200:
        abort(404, "User does not exists")

    response = json.loads(resp.content.decode())
    genre_list = []

    for filme in response.get("movieList"):
        jaVistos.append(int(filme))
        r = http_request_with_jwt_complete('http://34.120.57.34/gestaotitles/movies/' + str(filme))

        # old r, if needed to check anything, just comment the above and uncomment below one
        # r = requests.get('http://34.120.57.34/gestaotitles/movies/' + str(filme))
        responseFilme = json.loads(r.content.decode())
        if (len(responseFilme.get("movie_genre")) > 0):
            for genre in responseFilme.get("movie_genre"):
                genre_list.append(genre.get("genre").get("genre_name"))

    if (len(genre_list) == 0):
        abort(404, "Cannot recommend movies because user has not seen movies")

    lista_genero = most_frequent(genre_list)

    resposta = []
    for genero in lista_genero:

        respGenre = http_request_with_jwt_complete(
            'http://34.120.57.34/gestaotitles/movies/filtered?primaryTitle=&&genre=' + str(
                genero) + '&&region=&&language=&&startYear=')

        # old respGenre, if needed to check anything, just comment the above and uncomment below one
        # respGenre = requests.get('http://34.120.57.34/gestaotitles/movies/filtered?primaryTitle=&&genre=' + str(genero) + '&&region=&&language=&&startYear=')

        responseGenre = json.loads(respGenre.content.decode())

        # resposta = []

        if len(responseGenre) > 15:
            for r in range(15):
                filme_id = int(responseGenre[r].get("tconst"))
                if filme_id not in jaVistos:
                    if len(resposta) < 5:
                        resposta.append(responseGenre[r])
        else:
            for r in range(len(responseGenre)):
                filme_id = int(responseGenre[r].get("tconst"))
                if filme_id not in jaVistos:
                    if len(resposta) < 5:
                        resposta.append(responseGenre[r])

    # verificar esse resposta dentro do for: nao deveria estar fora do for? Pus fora do for
    if len(resposta) == 0:
        data = make_response(json.dumps({"resposta": "Nao existem filmes para recomendar"}))
        data.status_code = 200

        return data
    else:
        data = make_response(json.dumps(resposta))
        data.status_code = 200

        return data


def most_frequent(List):
    counter = 0
    generos = []

    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency >= counter:
            counter = curr_frequency
            generos.append(i)

    return generos  # []


def http_request_with_jwt_complete(request_url):
    # Starts with Authentication Part: Must have the key to use
    # Key is local, this is insecure, but for development it is okay
    # Need to see if the key format is right. It should be, it is from tutorial directly
    sa_keyfile = open("unified-sa-authorization-keys.json", "r")
    my_temp_jwt = generate_jwt(sa_keyfile, audience="http://imoviesforyou.me/recomendacoes")
    sa_keyfile.close()

    resp = make_jwt_request(my_temp_jwt, request_url)
    return resp
