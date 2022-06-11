import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector.constants import ClientFlag

#genre = pd.read_csv("genre.csv" , low_memory=False)
#movie_genre = pd.read_csv("movie_genre.csv" , low_memory=False)
title_akas = pd.read_csv("title.akas.csv" , low_memory=False)
title_akas['titleId']=title_akas['titleId'].astype(float).astype("Int64")
title_akas['ordering']=title_akas['ordering'].astype(float).astype("Int64")


# title_basics = pd.read_csv("title.basics.csv" , low_memory=False)
# title_basics['runtimeMinutes']=title_basics['runtimeMinutes'].replace(to_replace = r'\N', value = -1)
# title_basics['runTime']=title_basics['runTime'].astype(float).astype("Int64")
# title_basics['isAdult']=title_basics['isAdult'].astype(float).astype("Int64")
# title_basics['tconst']=title_basics['tconst'].astype(float).astype("Int64")

#title_ratings = pd.read_csv("title.ratings.csv" , low_memory=False)


config = {
    'user': 'root',
    'password': 'carapau2021',
    'host': '35.242.233.217'
    # 'client_flags': [ClientFlag.SSL],
    # 'ssl_ca': 'ssl/server-ca.pem',
    # 'ssl_cert': 'ssl/client-cert.pem',
    # 'ssl_key': 'ssl/client-key.pem'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)

config['database'] = 'gestaofilmes'  # add new database to config dict
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()


##########################GENRE###############################
# cursor.execute("DELETE FROM genre_csv")
# cnxn.commit()  # and commit changes

# # first we setup our query
# query = ("INSERT INTO genre_csv (genre_id,genre_name) VALUES (%s, %s)")
# lista=list(genre.to_records(index=False))

# # then we execute with every row in our dataframe
# # #print(type(int(lista[0][0])))
# for row in lista:
#     #print((int(row[0]),row[1]))
#     cursor.execute(query, (int(row[0]),row[1]))

# # # cursor.executemany(query, list(genre.to_records(index=False)))
# cnxn.commit()  # and commit changes

# cursor.execute("SELECT * FROM genre_csv")

# out = cursor.fetchall()
# for row in out:
#     print(row)

#############################movies################################

cursor.execute("DELETE FROM title_akas_csv")
cnxn.commit()  # and commit changes
# cursor.execute("ALTER TABLE title_basics_csv MODIFY primaryTitle VARCHAR(1000)")
# cnxn.commit()  # and commit changes

#cursor.execute("CREATE TABLE title_basics_csv (tconst INT NOT NULL AUTO_INCREMENT,titleType VARCHAR(100),primaryTitle VARCHAR(400),isAdult INT,startYear VARCHAR(4),endYear VARCHAR(4),runTime INT, PRIMARY KEY(tconst));")

# first we setup our query
query = ("INSERT INTO title_akas_csv (titleId,ordering,title,region,language) VALUES (%s, %s, %s, %s, %s)")
lista=list(title_akas.to_records(index=False))

# then we execute with every row in our dataframe
# print(type(lista[0][0])) #0
# print(type(lista[0][3])) #3
# print(type(lista[0][4])) #4
# print(type(lista[1][6])) #6

for row in lista:
    print((row[0],row[1],row[2],row[3],row[4]))
    cursor.execute(query, ((row[0],row[1],row[2],row[3],row[4])))

# cursor.executemany(query, list(title_basics.to_records(index=False)))
cnxn.commit()  # and commit changes

# cursor.execute("SELECT * FROM title_basics_csv")

# out = cursor.fetchall()
# for row in out:
#     print(row)