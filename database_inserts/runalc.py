import sqlalchemy
import numpy as np
import pandas as pd

#genre = pd.read_csv("genre.csv" , low_memory=False)

######

movie_genre = pd.read_csv("movie_genre.csv" , low_memory=False)
# print(movie_genre[movie_genre['tconst']>7219786])
movie_genre['genre_id']=movie_genre['gconst']
movie_genre=movie_genre.drop(columns=['gconst'])
movie_genre['genre_id']=movie_genre['genre_id'].astype(float).astype("Int64")
movie_genre['tconst']=movie_genre['tconst'].astype(float).astype("Int64")
#######

title_akas = pd.read_csv("title.akas.csv" , low_memory=False)
title_akas['titleId']=title_akas['titleId'].astype(float).astype("Int64")
title_akas['ordering']=title_akas['ordering'].astype(float).astype("Int64")

#####
title_basics = pd.read_csv("title.basics.csv" , low_memory=False)

title_basics['primaryTitle'] = title_basics['primaryTitle'].replace(',','', regex=True)
title_basics['primaryTitle'] = title_basics['primaryTitle'].replace('""','', regex=True)
title_basics['primaryTitle'] = title_basics['primaryTitle'].replace(';','', regex=True)

title_basics['runTime']=title_basics['runtimeMinutes']
title_basics=title_basics.drop(columns=['genres','runtimeMinutes'])

title_basics['runTime'] .loc[title_basics['runTime'] =="Reality-TV"] = -1
title_basics['runTime'] .loc[title_basics['runTime'] =="Talk-Show"] = -1
title_basics['runTime'] .loc[title_basics['runTime'] =="Animation,Family"] = -1
title_basics['runTime'] .loc[title_basics['runTime'] =="Animation,Comedy,Drama"] = -1


title_basics['runTime']=title_basics['runTime'].replace(to_replace = r'\N', value = -1)
title_basics['runTime']=title_basics['runTime'].astype(float).astype("Int64")
title_basics['isAdult']=title_basics['isAdult'].astype(float).astype("Int64")
title_basics['tconst']=title_basics['tconst'].astype(float).astype("Int64")
# print(title_basics[title_basics['tconst'] ==-1])
########
# tconst,averageRating,numVotes
title_ratings = pd.read_csv("title.ratings.csv" , low_memory=False)
title_ratings['tconst']=title_ratings['tconst'].astype(float).astype("Int64")
title_ratings['averageRating']=title_ratings['averageRating'].astype(float)
title_ratings['numVotes']=title_ratings['numVotes'].astype(float).astype("Int64")

########

database_username = 'root'
database_password = 'carapau2021'
database_ip       = '35.242.233.217'
database_name     = 'classifications'

database_connection = sqlalchemy.create_engine(
    'mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(
        database_username, 
        database_password,
        database_ip, database_name
    ), pool_recycle=3600, pool_size=4).connect()
title_basics.to_sql(
    con=database_connection, 
    name='title_basics_csv', 
    if_exists='append',
    chunksize=1000,
    index=False
)

title_akas.to_sql(
    con=database_connection, 
    name='title_akas2_csv', 
    if_exists='append',
    chunksize=1000,
    index=False
)
result = database_connection.execute("INSERT IGNORE INTO title_akas_csv SELECT * FROM title_akas2_csv")
database_connection.close()
movie_genre.to_sql(
    con=database_connection, 
    name='movie_genre_csv', 
    if_exists='append',
    chunksize=1000,
    index=False
)

title_ratings.to_sql(
    con=database_connection, 
    name='classification', 
    if_exists='append',
    chunksize=1000,
    index=False
)

title_basics.to_sql(
    con=database_connection, 
    name='title_basics_csv', 
    if_exists='append',
    chunksize=1000,
    index=False
)