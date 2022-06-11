#!/bin/bash
cd ms_classificacoes
docker build -t classificacoes:latest .
cd ../ms_filmes
docker build -t getfilmes:latest .
cd ../ms_gestaocontas
docker build -t gestaocontas:latest .
cd ../ms_gestaofilmes
docker build -t gestaofilmes:latest .
cd ../ms_recomendacoes
docker build -t recomendacoes:latest .

docker run --name classificacoes -it -d --net host classificacoes
docker run --name getfilmes -it -d --net host getfilmes
docker run --name gestaocontas -it -d --net host gestaocontas
docker run --name gestaofilmes -it -d --net host gestaofilmes
docker run --name recomendacoes -it -d --net host recomendacoes
