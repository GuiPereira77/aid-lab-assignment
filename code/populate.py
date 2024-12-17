import pandas as pd
import pymysql
from sqlalchemy import create_engine

db_user = 'aid'
db_password = '123456'
db_host = 'localhost:3306'
db_name = 'aid'

current_row = ''

engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}')

file_path = './data/final_data.csv'
df = pd.read_csv(file_path)
df.fillna(value="", inplace=True)

def get_or_create(cursor, table, column, value):
    cursor.execute(f"SELECT {table}_id FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s)", (value,))
    return cursor.lastrowid

def convert_string_to_number(s):
    units = {
        'k': 1000,
        'm': 1000000,
        'b': 1000000000
    }

    try:
        unit = s[-1].lower()
        number = float(s[:-1])

        if unit in units:
            return int(number * units[unit])

        return int(s)
    except:
        return None

def process_rating(rating):
    if rating == 'no-rating':
        return None
    return rating

try:
    with engine.connect() as conn:
        conn = conn.execution_options(autocommit=True)
        with conn.connection.cursor() as cursor:
            for index, row in df.iterrows():
                #if index > 500: #used for testing
                #    break

                if index % 100 == 0:
                    print("Current index: " + str(index))
                    cursor.execute("SELECT COUNT(*) FROM movie")
                    print("Rows in movie table:", cursor.fetchone()[0])

                tagline = ''
                if(row['Taglines'] != None or row['Taglines'] != 'NaN'):
                    tagline = row['Taglines']

                current_row = row
                
                director_id = get_or_create(cursor, 'director', 'director_name', row['Director'])
                writer_id = get_or_create(cursor, 'writer', 'writer_name', row['Writer'])
                year = int(row['year'])
                cursor.execute("INSERT IGNORE INTO year (year) VALUES (%s)", (year,))

                cursor.execute("""
                    INSERT INTO movie (
                        movie_title, overview, director_id, writer_id, year, rating, user_rating,
                        popularity_score, vote_count, path, adult, poster_image, runtime, taglines
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['movie title'], row['Overview'], director_id, writer_id, year, process_rating(row['Rating']), 
                    convert_string_to_number(row['User Rating']), row['Popularity'], row['Votes'], row['path'], row['Adult'], 
                    row['Poster Image'], row['Runtime'], tagline
                ))
                movie_id = cursor.lastrowid
                
                genres = eval(row['Generes'])
                for genre in genres:
                    genre_id = get_or_create(cursor, 'genre', 'genre_name', genre)
                    cursor.execute("""
                        INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)
                    """, (movie_id, genre_id))

                keywords = eval(row['Keywords'])
                for keyword in keywords:
                    keyword_id = get_or_create(cursor, 'keyword', 'keyword_name', keyword)
                    cursor.execute("""
                        INSERT IGNORE INTO movie_keyword (movie_id, keyword_id) VALUES (%s, %s)
                    """, (movie_id, keyword_id))

                actors = eval(row['Top 5 Casts'])
                for actor in actors:
                    actor_id = get_or_create(cursor, 'actor', 'actor_name', actor)
                    cursor.execute("""
                        INSERT IGNORE INTO movie_actor (movie_id, actor_id) VALUES (%s, %s)
                    """, (movie_id, actor_id))

        conn.connection.commit()

except Exception as e:
        print(current_row)
        print(f"Error: {e}")
    
print("Database populated successfully!")
