import pandas as pd
import pymysql
from sqlalchemy import create_engine

db_user = 'aid'
db_password = '123456'
db_host = 'localhost:3306'
db_name = 'aid'

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

def execute_query(query, params=None):
    try:
        with engine.connect() as conn:
            conn = conn.execution_options(autocommit=True)
            with conn.connection.cursor() as cursor:
                cursor.execute(query, params)
                conn.connection.commit()
    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close

# 5.1 Actor-Genre Aggregate
def populate_actor_genre_aggregate():
    query = """
        INSERT INTO actor_genre (genre_id, actor_id, movie_count, avg_rating, avg_popularity)
        SELECT 
            mg.genre_id, ma.actor_id, 
            COUNT(m.movie_id) AS movie_count, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie m
        JOIN movie_genre mg ON m.movie_id = mg.movie_id
        JOIN movie_actor ma ON m.movie_id = ma.movie_id
        GROUP BY mg.genre_id, ma.actor_id;
    """
    execute_query(query)
    print("Actor-Genre Aggregate populated successfully!")

# 5.2 Keyword-Genre Aggregate
def populate_keyword_genre_aggregate():
    query = """
        INSERT INTO keyword_genre (genre_id, keyword_id, movie_count)
        SELECT 
            mg.genre_id, mk.keyword_id, 
            COUNT(m.movie_id) AS movie_count
        FROM movie m
        JOIN movie_genre mg ON m.movie_id = mg.movie_id
        JOIN movie_keyword mk ON m.movie_id = mk.movie_id
        GROUP BY mg.genre_id, mk.keyword_id;
    """
    execute_query(query)
    print("Keyword-Genre Aggregate populated successfully!")

# 5.3 Year-Genre Aggregate
def populate_year_genre_aggregate():
    query = """
        INSERT INTO yearly_genre (year, genre_id, movie_count, total_runtime, avg_runtime, avg_rating, avg_popularity)
        SELECT 
            m.year, mg.genre_id, 
            COUNT(m.movie_id) AS movie_count, 
            SUM(m.runtime) AS total_runtime, 
            AVG(m.runtime) AS avg_runtime, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie m
        JOIN movie_genre mg ON m.movie_id = mg.movie_id
        GROUP BY m.year, mg.genre_id;
    """
    execute_query(query)
    print("Year-Genre Aggregate populated successfully!")

# 5.4 Director-Genre Aggregate
def populate_director_genre_aggregate():
    query = """
        INSERT INTO director_genre (director_id, genre_id, movie_count, avg_runtime, avg_rating, avg_popularity)
        SELECT 
            m.director_id, mg.genre_id, 
            COUNT(m.movie_id) AS movie_count, 
            AVG(m.runtime) AS avg_runtime, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie m
        JOIN movie_genre mg ON m.movie_id = mg.movie_id
        GROUP BY m.director_id, mg.genre_id;
    """
    execute_query(query)
    print("Director-Genre Aggregate populated successfully!")

# 5.5 Movie Release Trend by Year
def populate_movie_release_trend():
    query = """
        INSERT INTO yearly_movie_release (year, adult_movie_count, non_adult_movie_count, total_movie_count, avg_runtime, avg_rating, avg_popularity)
        SELECT 
            m.year, 
            SUM(CASE WHEN m.adult = 1 THEN 1 ELSE 0 END) AS adult_movie_count, 
            SUM(CASE WHEN m.adult = 0 THEN 1 ELSE 0 END) AS non_adult_movie_count, 
            COUNT(m.movie_id) AS total_movie_count, 
            AVG(m.runtime) AS avg_runtime, 
            AVG(m.rating) AS avg_rating, 
            AVG(m.popularity_score) AS avg_popularity
        FROM movie m
        GROUP BY m.year;
    """
    execute_query(query)
    print("Movie Release Trend by Year populated successfully!")

def main():
    print("Populating Aggregate Tables...")
    populate_actor_genre_aggregate()
    populate_keyword_genre_aggregate()
    populate_year_genre_aggregate()
    populate_director_genre_aggregate()
    populate_movie_release_trend()
    print("All aggregate tables populated successfully!")

if __name__ == "__main__":
    main()
