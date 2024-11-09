# Dimensional Model

dimensional model for dataset in *dbdiagram syntax*:

```
// Dimension Tables
Table Time {
    time_id int [pk]
    year int
    month int
    day int
}

Table Movie {
    movie_id int [pk]
    movie_title varchar
    rating varchar
    overview text
    keywords text
    adult boolean
    runtime int
}

Table Director {
    director_id int [pk]
    director_name varchar
}

Table Genre {
    genre_id int [pk]
    genre_name varchar
}

Table Cast {
    cast_id int [pk]
    cast_name varchar
}

// Fact Tables
Table MovieRatings {
    rating_id int [pk]
    movie_id int [ref: > Movie.movie_id]
    time_id int [ref: > Time.time_id]
    average_rating float
    user_rating_count int
}

Table PopularityFact {
    popularity_id int [pk]
    movie_id int [ref: > Movie.movie_id]
    time_id int [ref: > Time.time_id]
    popularity_score float
}

Table VotesFact {
    vote_id int [pk]
    movie_id int [ref: > Movie.movie_id]
    time_id int [ref: > Time.time_id]
    vote_count int
}

// Relationships
Ref: MovieRatings.movie_id > Movie.movie_id
Ref: MovieRatings.time_id > Time.time_id
Ref: MovieRatings.movie_id > Director.director_id
Ref: MovieRatings.movie_id > Genre.genre_id
Ref: MovieRatings.movie_id > Cast.cast_id

Ref: PopularityFact.movie_id > Movie.movie_id
Ref: PopularityFact.time_id > Time.time_id
Ref: PopularityFact.movie_id > Director.director_id
Ref: PopularityFact.movie_id > Genre.genre_id
Ref: PopularityFact.movie_id > Cast.cast_id

Ref: VotesFact.movie_id > Movie.movie_id
Ref: VotesFact.time_id > Time.time_id
Ref: VotesFact.movie_id > Director.director_id
Ref: VotesFact.movie_id > Genre.genre_id
Ref: VotesFact.movie_id > Cast.cast_id
```

## Explanation
- **Dimension Tables**: Represent `Time`, `Movie`, `Director`, `Genre`, and `Cast`, containing primary attributes for each entity.
- **Fact Tables**: Represent `MovieRatings`, `PopularityFact`, and `VotesFact` with measures and foreign keys pointing to dimensions.
- **Relationships**: Foreign keys define the relationships between fact and dimension tables. The fact tables are related to dimensions like `Time`, `Movie`, `Director`, `Genre`, and `Cast`.