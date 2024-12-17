USE aid;

-- Date Dimension
CREATE TABLE IF NOT EXISTS year (
    year INT PRIMARY KEY
);

-- Keyword Dimension
CREATE TABLE IF NOT EXISTS keyword (
    keyword_id INT PRIMARY KEY AUTO_INCREMENT,
    keyword_name VARCHAR(100)
);

-- Director Dimension
CREATE TABLE IF NOT EXISTS director (
    director_id INT PRIMARY KEY AUTO_INCREMENT,
    director_name VARCHAR(255)
);

-- Writer Dimension
CREATE TABLE IF NOT EXISTS writer (
    writer_id INT PRIMARY KEY AUTO_INCREMENT,
    writer_name VARCHAR(255)
);

-- Genre Dimension
CREATE TABLE IF NOT EXISTS genre (
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(50)
);

-- Actor Dimension
CREATE TABLE IF NOT EXISTS actor (
    actor_id INT PRIMARY KEY AUTO_INCREMENT,
    actor_name VARCHAR(255)
);

-- Movie Details Fact Table
CREATE TABLE IF NOT EXISTS movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_title VARCHAR(255),
    overview TEXT,
    director_id INT,
    writer_id INT,
    year INT,
    rating float,
    user_rating INT,
    popularity_score float,
    vote_count INT,
    path VARCHAR(500),
    adult BOOLEAN,
    poster_image VARCHAR(500),
    runtime INT,
    taglines VARCHAR(1000),
    
    FOREIGN KEY (director_id) REFERENCES director(director_id),
    FOREIGN KEY (writer_id) REFERENCES writer(writer_id),
    FOREIGN KEY (year) REFERENCES year(year)
);

-- Bridge Tables
CREATE TABLE IF NOT EXISTS movie_actor (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
);

CREATE TABLE IF NOT EXISTS movie_keyword (
    movie_id INT,
    keyword_id INT,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
);

CREATE TABLE IF NOT EXISTS movie_genre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

-- Aggregate Stars

-- Actor-Genre Aggregate
CREATE TABLE IF NOT EXISTS actor_genre (
    actor_genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_id INT,
    actor_id INT,
    movie_count INT,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
    FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
);

-- Keyword-Genre Aggregate
CREATE TABLE IF NOT EXISTS keyword_genre (
    keyword_genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_id INT,
    keyword_id INT,
    movie_count INT,
    
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
);

-- Yearly Genre Performance
CREATE TABLE IF NOT EXISTS yearly_genre (
    year_genre_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    genre_id INT,
    movie_count INT,
    total_runtime INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (year) REFERENCES year(year),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

-- Director-Genre Aggregate
CREATE TABLE IF NOT EXISTS director_genre (
    director_genre_id INT PRIMARY KEY AUTO_INCREMENT,
    director_id INT,
    genre_id INT,
    movie_count INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (director_id) REFERENCES director(director_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

-- Movie Release Trend
CREATE TABLE IF NOT EXISTS yearly_movie_release (
    year_movie_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    adult_movie_count INT,
    non_adult_movie_count INT,
    total_movie_count INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (year) REFERENCES year(year)
);