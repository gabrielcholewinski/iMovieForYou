/*MOVIES DB*/
CREATE TABLE title_basics_csv (tconst INT NOT NULL AUTO_INCREMENT,titleType VARCHAR(100),primaryTitle VARCHAR(1000),isAdult INT
,startYear VARCHAR(4),endYear VARCHAR(4),runTime INT, PRIMARY KEY(tconst));

CREATE TABLE genre_csv (genre_id INT NOT NULL AUTO_INCREMENT, genre_name VARCHAR(300), PRIMARY KEY(genre_id));


CREATE TABLE title_akas_csv (titleId INT NOT NULL, 
    ordering INT, title VARCHAR(1000), region VARCHAR(32), language VARCHAR(32),
    PRIMARY KEY(titleId, ordering), 
    FOREIGN KEY (titleId) REFERENCES title_basics_csv(tconst));

CREATE TABLE title_akas2_csv (titleId INT NOT NULL, 
    ordering INT, title VARCHAR(5000), region VARCHAR(32), language VARCHAR(32),
    PRIMARY KEY(titleId, ordering));    

CREATE TABLE title_ratings_csv (tconst INT NOT NULL, averageRating FLOAT, numVotes INT,
    PRIMARY KEY(tconst), FOREIGN KEY (tconst) REFERENCES title_basics_csv(tconst));

CREATE TABLE movie_genre_csv (genre_id INT NOT NULL, tconst INT NOT NULL, 
    PRIMARY KEY(tconst, genre_id), FOREIGN KEY (tconst) REFERENCES title_basics_csv(tconst),
    FOREIGN KEY (genre_id) REFERENCES genre_csv(genre_id));

/*CLASSIFICAOES DB*/
CREATE TABLE classification (tconst INT NOT NULL, averageRating FLOAT, numVotes INT,
    PRIMARY KEY(tconst));

CREATE TABLE userRating (user_id INT NOT NULL, tconst INT NOT NULL, rating FLOAT,
    PRIMARY KEY(user_id,tconst));

/*USER DB*/
CREATE TABLE user (user_id INT NOT NULL AUTO_INCREMENT, lname VARCHAR(32), fname VARCHAR(32), 
    username VARCHAR(32), password VARCHAR(32), PRIMARY KEY(user_id));

CREATE TABLE userMoviesList (user_id INT NOT NULL, movie INT NOT NULL, 
    PRIMARY KEY(user_id,movie), FOREIGN KEY (user_id) REFERENCES user(user_id));