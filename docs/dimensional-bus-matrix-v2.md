# Planning

> 1 star (Movie details), make use of bridge tables and agregations (e.g.: genre and year) to increase complexity

## 1. Dimensional Bus Matrix


| Table | Date | Keyword | Director | Writer | Genre | Actor |
| --- | --- | --- | --- | --- | --- | --- |
| Movie Fact | X | X | X | X | X | X |

Meter bridge tables?


## 2. Dimensions Dictionary

- **Date Dimension**:
  - `year` (year the movie was released)
  - `month` (if available from additional sources)
  - `day` (if available from additional sources)

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

- **Movie Details Fact Table**: This dimension captures the details of each movie.
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

## 4. Bridge Tables (not defined on matrix)

- MovieCast: connects the movies with it's top 5 cast
- MovieKeywords: connects the movies with it's keyword
- MovieGenres: connects the movies with it's genres

## 5. Agregation Star (?)

### 5.1 Aggregate Star: **Actor-Genre Aggregate**

Purpose: To analyze which actors frequently appear in certain genres, enabling a focus on actor popularity within genres.

- **Fact Table**: Actor-Genre Aggregate
    - `actor_genre_agg_id` (unique identifier for each record)
    - `genre_id` (FK to Genre Dimension)
    - `cast_id` (FK to Actor Dimension)
    - `movie_count` (count of movies for this actor in this genre)
    - `avg_runtime` (average runtime of movies for this actor in this genre)
- **Dimensions**:
    - Actor Dimension
    - Genre Dimension

### 5.2 Aggregate Star: **Keyword-Genre Aggregate**

Purpose: Provides insight into how certain keywords are distributed across genres, useful for understanding thematic associations.

- **Fact Table**: Keyword-Genre Aggregate
    - `keyword_genre_agg_id` (unique identifier for each record)
    - `genre_id` (FK to Genre Dimension)
    - `keyword_id` (FK to Keyword Dimension)
    - `movie_count` (number of movies in this genre with this keyword)
- **Dimensions**:
    - Keyword Dimension
    - Genre Dimension

### 5.3 Aggregate Star: **Yearly Genre Performance**

Purpose: Tracks the yearly popularity and volume of each genre.

- **Fact Table**: Yearly Genre Performance
    - `year_genre_agg_id` (unique identifier for each record)
    - `year` (from Date Dimension)
    - `genre_id` (FK to Genre Dimension)
    - `movie_count` (number of movies in this genre in that year)
    - `total_runtime` (sum of runtimes for movies in this genre and year)
    - `avg_runtime` (average runtime of movies in this genre and year)
- **Dimensions**:
    - Date Dimension
    - Genre Dimension

### 5.4 Aggregate Star: **Director-Genre Aggregate**

Purpose: Shows which directors are most active or successful in specific genres, providing insight into genre specialization.

- **Fact Table**: Director-Genre Aggregate
    - `director_genre_agg_id` (unique identifier for each record)
    - `director_id` (FK to Director Dimension)
    - `genre_id` (FK to Genre Dimension)
    - `movie_count` (number of movies directed in this genre)
    - `avg_runtime` (average runtime of movies directed in this genre)
- **Dimensions**:
    - Director Dimension
    - Genre Dimension

### 5.5 Aggregate Star: **Movie Release Trend by Year**

Purpose: Tracks the volume and distribution of movies released each year, potentially segmented by various attributes such as adult classification.

- **Fact Table**: Yearly Movie Release Aggregate
    - `year_movie_agg_id` (unique identifier for each record)
    - `year` (from Date Dimension)
    - `adult_movie_count` (count of movies marked as adult)
    - `non_adult_movie_count` (count of non-adult movies)
    - `total_movie_count` (total count of movies)
- **Dimensions**:
    - Date Dimension