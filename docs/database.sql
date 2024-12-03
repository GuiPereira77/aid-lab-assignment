-- Date Dimension
CREATE TABLE dim_date (
    year INT PRIMARY KEY
);

-- Keyword Dimension
CREATE TABLE dim_keyword (
    keyword_id INT PRIMARY KEY AUTO_INCREMENT,
    keyword_name VARCHAR(100)
);

-- Director Dimension
CREATE TABLE dim_director (
    director_id INT PRIMARY KEY AUTO_INCREMENT,
    director_name VARCHAR(255)
);

-- Writer Dimension
CREATE TABLE dim_writer (
    writer_id INT PRIMARY KEY AUTO_INCREMENT,
    writer_name VARCHAR(255)
);

-- Genre Dimension
CREATE TABLE dim_genre (
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(50)
);

-- Actor Dimension
CREATE TABLE dim_actor (
    cast_id INT PRIMARY KEY AUTO_INCREMENT,
    cast_name VARCHAR(255)
);

-- Movie Details Fact Table
CREATE TABLE fact_movie (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    movie_tile VARCHAR(255),
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
    taglines TEXT,
    
    FOREIGN KEY (director_id) REFERENCES dim_director(director_id),
    FOREIGN KEY (writer_id) REFERENCES dim_writer(writer_id),
    FOREIGN KEY (year) REFERENCES dim_date(year)
);

-- Bridge Tables
CREATE TABLE bridge_movie_cast (
    movie_id INT,
    cast_id INT,
    PRIMARY KEY (movie_id, cast_id),
    FOREIGN KEY (movie_id) REFERENCES fact_movie(movie_id),
    FOREIGN KEY (cast_id) REFERENCES dim_actor(cast_id)
);

CREATE TABLE bridge_movie_keyword (
    movie_id INT,
    keyword_id INT,
    PRIMARY KEY (movie_id, keyword_id),
    FOREIGN KEY (movie_id) REFERENCES fact_movie(movie_id),
    FOREIGN KEY (keyword_id) REFERENCES dim_keyword(keyword_id)
);

CREATE TABLE bridge_movie_genre (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES fact_movie(movie_id),
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
);

-- Aggregate Stars

-- Actor-Genre Aggregate
CREATE TABLE agg_actor_genre (
    actor_genre_agg_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_id INT,
    cast_id INT,
    movie_count INT,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id),
    FOREIGN KEY (cast_id) REFERENCES dim_actor(cast_id)
);

-- Keyword-Genre Aggregate
CREATE TABLE agg_keyword_genre (
    keyword_genre_agg_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_id INT,
    keyword_id INT,
    movie_count INT,
    
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id),
    FOREIGN KEY (keyword_id) REFERENCES dim_keyword(keyword_id)
);

-- Yearly Genre Performance
CREATE TABLE agg_yearly_genre (
    year_genre_agg_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    genre_id INT,
    movie_count INT,
    total_runtime INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (year) REFERENCES dim_date(year),
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
);

-- Director-Genre Aggregate
CREATE TABLE agg_director_genre (
    director_genre_agg_id INT PRIMARY KEY AUTO_INCREMENT,
    director_id INT,
    genre_id INT,
    movie_count INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (director_id) REFERENCES dim_director(director_id),
    FOREIGN KEY (genre_id) REFERENCES dim_genre(genre_id)
);

-- Movie Release Trend
CREATE TABLE agg_yearly_movie_release (
    year_movie_agg_id INT PRIMARY KEY AUTO_INCREMENT,
    year INT,
    adult_movie_count INT,
    non_adult_movie_count INT,
    total_movie_count INT,
    avg_runtime float,
    avg_rating float,
    avg_popularity float,
    
    FOREIGN KEY (year) REFERENCES dim_date(year)
);