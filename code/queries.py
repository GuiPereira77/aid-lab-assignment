import os
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(filename="query_errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

# Load credentials from environment variables
db_user = os.getenv('DB_USER', 'aid')
db_password = os.getenv('DB_PASSWORD', '123456')  # Replace with secure handling
db_host = os.getenv('DB_HOST', 'localhost:3306')
db_name = os.getenv('DB_NAME', 'aid')

# Create database engine
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

# Ensure CSV directory exists
csv_path = './data/csv/'
os.makedirs(csv_path, exist_ok=True)

def execute_query(query, params=None, output_csv=None):
    """Executes a SQL query and saves the output to a CSV file if specified."""
    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params=params)
            if output_csv:
                df.to_csv(os.path.join(csv_path, output_csv), index=False)
            return df
    except Exception as e:
        logging.error(f"Query Execution Error: {e}")
        print(f"Error: {e}")

# -------------------------------------------
# Query Functions
# -------------------------------------------

def movie_count():
    """Fetches movie statistics and saves to CSV."""
    query = """
        SELECT 
            COUNT(movie_id) AS movie_count,
            MAX(rating) AS max_rating,
            MIN(rating) AS min_rating,
            AVG(rating) AS avg_rating,
            MAX(user_rating) AS max_user_rating,
            MIN(user_rating) AS min_user_rating,
            AVG(user_rating) AS avg_user_rating,
            MAX(popularity_score) AS max_popularity_score,
            MIN(popularity_score) AS min_popularity_score,
            AVG(popularity_score) AS avg_popularity_score,
            MAX(vote_count) AS max_vote_count,
            MIN(vote_count) AS min_vote_count,
            AVG(vote_count) AS avg_vote_count
        FROM movie;
    """
    execute_query(query, None, 'movie_table_stats.csv')
    print("Movie count query executed successfully.")

def top_rated_movies(limit=10):
    """Fetches the top-rated movies."""
    query = f"""
        SELECT 
            movie_title, 
            rating, 
            user_rating, 
            popularity_score 
        FROM movie 
        ORDER BY rating DESC, vote_count DESC 
        LIMIT {limit};
    """
    execute_query(query, None, 'top_rated_movies.csv')
    print(f"Top {limit} rated movies fetched successfully.")

def most_popular_movies(limit=10):
    """Fetches the most popular movies based on popularity score."""
    query = f"""
        SELECT 
            movie_title, 
            popularity_score, 
            rating, 
            vote_count 
        FROM movie 
        ORDER BY popularity_score DESC 
        LIMIT {limit};
    """
    execute_query(query, None, 'most_popular_movies.csv')
    print(f"Top {limit} most popular movies fetched successfully.")

def top_directors_by_avg_rating(limit=10):
    """Fetches the top directors by average movie rating."""
    query = f"""
        SELECT 
            d.director_name, 
            COUNT(m.movie_id) AS movie_count, 
            AVG(m.rating) AS avg_rating 
        FROM director d
        JOIN movie m ON d.director_id = m.director_id 
        GROUP BY d.director_name 
        ORDER BY avg_rating DESC 
        LIMIT {limit};
    """
    execute_query(query, None, 'top_directors_by_avg_rating.csv')
    print(f"Top {limit} directors by average rating fetched successfully.")

def genre_popularity():
    """Fetches genre popularity based on number of movies and average ratings."""
    query = """
        SELECT 
            g.genre_name, 
            COUNT(mg.movie_id) AS movie_count, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie_genre mg
        JOIN genre g ON mg.genre_id = g.genre_id
        JOIN movie m ON mg.movie_id = m.movie_id
        GROUP BY g.genre_name
        ORDER BY movie_count DESC;
    """
    execute_query(query, None, 'genre_popularity.csv')
    print("Genre popularity analysis completed.")

def actor_performance(limit=10):
    """Fetches actors with the highest average movie rating."""
    query = f"""
        SELECT 
            a.actor_name, 
            COUNT(ma.movie_id) AS movie_count, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie_actor ma
        JOIN actor a ON ma.actor_id = a.actor_id
        JOIN movie m ON ma.movie_id = m.movie_id
        GROUP BY a.actor_name
        HAVING movie_count > 2
        ORDER BY avg_rating DESC, movie_count DESC
        LIMIT {limit};
    """
    execute_query(query, None, 'top_actors_by_rating.csv')
    print(f"Top {limit} actors by rating fetched successfully.")

def yearly_trend():
    """Fetches movie release trends by year."""
    query = """
        SELECT 
            y.year, 
            COUNT(m.movie_id) AS total_movies, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie m
        JOIN year y ON m.year = y.year
        GROUP BY y.year
        ORDER BY y.year DESC;
    """
    execute_query(query, None, 'yearly_movie_trend.csv')
    print("Yearly movie trend analysis completed.")

def adult_vs_non_adult_trend():
    """Fetches the trend of adult vs. non-adult movies over time."""
    query = """
        SELECT 
            y.year, 
            SUM(CASE WHEN m.adult = TRUE THEN 1 ELSE 0 END) AS adult_movies,
            SUM(CASE WHEN m.adult = FALSE THEN 1 ELSE 0 END) AS non_adult_movies,
            COUNT(m.movie_id) AS total_movies
        FROM movie m
        JOIN year y ON m.year = y.year
        GROUP BY y.year
        ORDER BY y.year DESC;
    """
    execute_query(query, None, 'adult_vs_non_adult_trend.csv')
    print("Adult vs. non-adult movie trend analysis completed.")

def top_movie_per_year():
    """Finds the highest-rated movie for each year using window functions."""
    query = """
        SELECT year, movie_title, rating
        FROM (
            SELECT 
                m.year, 
                m.movie_title, 
                m.rating,
                RANK() OVER (PARTITION BY m.year ORDER BY m.rating DESC, m.vote_count DESC) AS ranked_position
            FROM movie m
        ) ranked
        WHERE ranked_position = 1;
    """
    execute_query(query, None, 'top_movie_per_year.csv')
    print("Top movie per year analysis completed.")

def genre_trend_over_time():
    """Tracks how each genre's popularity has evolved over time."""
    query = """
        SELECT 
            y.year, 
            g.genre_name, 
            COUNT(mg.movie_id) AS movie_count, 
            AVG(m.rating) AS avg_rating
        FROM movie_genre mg
        JOIN genre g ON mg.genre_id = g.genre_id
        JOIN movie m ON mg.movie_id = m.movie_id
        JOIN year y ON m.year = y.year
        GROUP BY y.year, g.genre_name
        ORDER BY y.year DESC, movie_count DESC;
    """
    execute_query(query, None, 'genre_trend_over_time.csv')
    print("Genre trend analysis completed.")

def most_consistent_directors(min_movies=5):
    """Finds directors with the most consistent high-rated movies."""
    query = f"""
        SELECT 
            d.director_name, 
            COUNT(m.movie_id) AS movie_count, 
            ROUND(STDDEV(m.rating), 2) AS rating_std_dev, 
            ROUND(AVG(m.rating), 2) AS avg_rating
        FROM director d
        JOIN movie m ON d.director_id = m.director_id
        GROUP BY d.director_name
        HAVING COUNT(m.movie_id) >= {min_movies}
        ORDER BY rating_std_dev ASC, avg_rating DESC
        LIMIT 10;
    """
    execute_query(query, None, 'most_consistent_directors.csv')
    print("Most consistent directors analysis completed.")

def breakout_actors():
    """Finds actors who had a significant increase in movie ratings over time."""
    query = """
        SELECT 
            a.actor_name, 
            first_movie.year AS debut_year, 
            last_movie.year AS latest_year, 
            ROUND(first_movie.avg_rating, 2) AS debut_avg_rating, 
            ROUND(last_movie.avg_rating, 2) AS latest_avg_rating, 
            ROUND(last_movie.avg_rating - first_movie.avg_rating, 2) AS rating_growth
        FROM 
            (SELECT ma.actor_id, MIN(m.year) AS year, AVG(m.rating) AS avg_rating 
             FROM movie_actor ma 
             JOIN movie m ON ma.movie_id = m.movie_id 
             GROUP BY ma.actor_id, m.year) first_movie
        JOIN 
            (SELECT ma.actor_id, MAX(m.year) AS year, AVG(m.rating) AS avg_rating 
             FROM movie_actor ma 
             JOIN movie m ON ma.movie_id = m.movie_id 
             GROUP BY ma.actor_id, m.year) last_movie
        ON first_movie.actor_id = last_movie.actor_id
        JOIN actor a ON first_movie.actor_id = a.actor_id
        WHERE first_movie.year < last_movie.year
        ORDER BY rating_growth DESC
        LIMIT 10;
    """
    execute_query(query, None, 'breakout_actors.csv')
    print("Breakout actors analysis completed.")

def highest_grossing_genres():
    """Ranks genres based on the highest cumulative popularity and vote count."""
    query = """
        SELECT 
            g.genre_name, 
            COUNT(mg.movie_id) AS movie_count, 
            SUM(m.popularity_score) AS total_popularity, 
            SUM(m.vote_count) AS total_votes
        FROM movie_genre mg
        JOIN genre g ON mg.genre_id = g.genre_id
        JOIN movie m ON mg.movie_id = m.movie_id
        GROUP BY g.genre_name
        ORDER BY total_popularity DESC, total_votes DESC;
    """
    execute_query(query, None, 'highest_grossing_genres.csv')
    print("Highest grossing genres analysis completed.")

def underrated_movies():
    """Finds highly rated movies with low popularity scores."""
    query = """
        SELECT 
            movie_title, 
            rating, 
            popularity_score, 
            vote_count
        FROM movie
        WHERE rating > 8.0 AND popularity_score < (SELECT AVG(popularity_score) FROM movie)
        ORDER BY rating DESC, popularity_score ASC;
    """
    execute_query(query, None, 'underrated_movies.csv')
    print("Underrated movies analysis completed.")


# -------------------------------------------
# Main Execution
# -------------------------------------------
def main():
    print("Starting query execution...")
    
    movie_count()
    top_rated_movies()
    most_popular_movies()
    top_directors_by_avg_rating()
    genre_popularity()
    actor_performance()
    yearly_trend()
    adult_vs_non_adult_trend()
    top_movie_per_year()
    genre_trend_over_time()
    most_consistent_directors()
    breakout_actors()
    highest_grossing_genres()
    underrated_movies()
    
    print("Query execution completed.")

if __name__ == "__main__":
    main()
    engine.dispose()  # Close database connection
