# Planning

## 1. Dimensional Bus Matrix

| Fact Table    | Date | Movie | Keyword | Director | Writer | Genre | Actor |
| ---           | ---  | ---   | ---     | ---      | ---    | ---   | ---   |
| Movie Details | X    | X     | X       | X        | X      | X     | X     |
| Movie Rating  |      | X     |         |          |        |       |       |
| Popularity    |      |       |         |          |        |       |       |
| Vote          |      |       |         |          |        |       |       |

## 2. Dimensions Dictionary

> *! in the data we only have access to the movie's release year*
- **Date Dimension**:
  - `year` (year the movie was released)
  - `month` (if available from additional sources)
  - `day` (if available from additional sources)

- **Movie Dimension**: This dimension captures the details of each movie.
  - `movie_id` (unique identifier for each movie)
  - `movie_tile`
  - `overview` (description of the movie)
  - `director_id` (fk to *Movie Dimension*)
  - `writer_id` (fk to *Writer Dimension*)
  - `year` (release year)
  - `path` (path to the movie)
  - `adult` (boolean indicating if the movie is intended for adults)
  - `poster_image` (path to the poster image)
  - `runtime` (movie's duration time)
  - `taglines (?)`

- **Keyword Dimension**: Captures details about keywords.
  - `keyword_id` (unique identifier)
  - `keyword_name`

- **Director Dimension**: Captures details about directors.
  - `director_id` (unique identifier)
  - `director_name`
  
- **Writer Dimension**: Captures details about writers.
  - `writer_id` (unique identifier)
  - `writer_name`

- **Genre Dimension**: Stores movie genres. Since each movie can have multiple genres, this can be a separate dimension.
  - `genre_id` (unique identifier)
  - `genre_name`

- **Actor Dimension**: Contains information on main cast members.
  - `cast_id` (unique identifier)
  - `cast_name`

## 3. Facts Dictionary

- **Movie Ratings Fact Table**: Tracks the user ratings for each movie.
  - `rating` (average rating of the movie)
  - `user_rating` (number of ratings given by users)
  - `movie_id` (foreign key to Movie Dimension)
  - `time_id` (foreign key to Time Dimension)

- **Popularity Fact Table**: Tracks popularity metrics over time.
  - `popularity_score` (numeric, from `Popularity`)
  - `movie_id` (foreign key to Movie Dimension)
  - `time_id` (foreign key to Time Dimension)

- **Vote Fact Table**: Stores the count of votes per movie.
  - `vote_count` (numeric, from `Votes`)
  - `movie_id` (foreign key to Movie Dimension)
  - `time_id` (foreign key to Time Dimension)

## 4. Bridge Tables (not defined on matrix)

- MovieCast: connects the movies with it's top 5 cast
- MovieKeywords: connects the movies with it's keyword
- MovieGenres: connects the movies with it's genres

estrelas agregadas por ano/genero (e.g.)