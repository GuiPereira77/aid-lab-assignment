import pandas as pd
import pymysql
from sqlalchemy import create_engine

db_user = 'aid'
db_password = '123456'
db_host = 'localhost:3306'
db_name = 'aid'

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

file_path = '../data/final_data.csv'
df = pd.read_csv(file_path)

def get_or_create(cursor, table, column, value):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))
    return cursor.lastrowid

with engine.connect() as conn:
    conn = conn.execution_options(autocommit=True)
    with conn.connection.cursor() as cursor:
        for index, row in df.iterrows():
            
            director_id = get_or_create(cursor, 'dim_director', 'director_name', row['Director'])
            writer_id = get_or_create(cursor, 'dim_writer', 'writer_name', row['Writer'])
            year = int(row['year'])
            cursor.execute("INSERT IGNORE INTO dim_date (year) VALUES (%s)", (year,))

            cursor.execute("""
                INSERT INTO fact_movie (
                    movie_tile, overview, director_id, writer_id, year, rating, user_rating,
                    popularity_score, vote_count, path, adult, poster_image, runtime, taglines
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['movie title'], row['Overview'], director_id, writer_id, year, row['Rating'], 
                row['User Rating'], row['Popularity'], row['Votes'], row['path'], row['Adult'], 
                row['Poster Image'], row['Runtime'], row['Taglines']
            ))
            movie_id = cursor.lastrowid
            
            genres = eval(row['Generes'])
            for genre in genres:
                genre_id = get_or_create(cursor, 'dim_genre', 'genre_name', genre)
                cursor.execute("""
                    INSERT IGNORE INTO bridge_movie_genre (movie_id, genre_id) VALUES (%s, %s)
                """, (movie_id, genre_id))

            keywords = eval(row['Keywords'])
            for keyword in keywords:
                keyword_id = get_or_create(cursor, 'dim_keyword', 'keyword_name', keyword)
                cursor.execute("""
                    INSERT IGNORE INTO bridge_movie_keyword (movie_id, keyword_id) VALUES (%s, %s)
                """, (movie_id, keyword_id))

            actors = eval(row['Top 5 Casts'])
            for actor in actors:
                actor_id = get_or_create(cursor, 'dim_actor', 'actor_name', actor)
                cursor.execute("""
                    INSERT IGNORE INTO bridge_movie_cast (movie_id, actor_id) VALUES (%s, %s)
                """, (movie_id, actor_id))

print("Database populated successfully!")
