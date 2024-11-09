CREATE TABLE `Time` (
  `time_id` int PRIMARY KEY,
  `year` int,
  `month` int,
  `day` int
);

CREATE TABLE `Movie` (
  `movie_id` int PRIMARY KEY,
  `movie_title` varchar(255),
  `rating` varchar(255),
  `overview` text,
  `keywords` text,
  `adult` boolean,
  `runtime` int
);

CREATE TABLE `Director` (
  `director_id` int PRIMARY KEY,
  `director_name` varchar(255)
);

CREATE TABLE `Genre` (
  `genre_id` int PRIMARY KEY,
  `genre_name` varchar(255)
);

CREATE TABLE `Cast` (
  `cast_id` int PRIMARY KEY,
  `cast_name` varchar(255)
);

CREATE TABLE `MovieRatings` (
  `rating_id` int PRIMARY KEY,
  `movie_id` int,
  `time_id` int,
  `average_rating` float,
  `user_rating_count` int
);

CREATE TABLE `PopularityFact` (
  `popularity_id` int PRIMARY KEY,
  `movie_id` int,
  `time_id` int,
  `popularity_score` float
);

CREATE TABLE `VotesFact` (
  `vote_id` int PRIMARY KEY,
  `movie_id` int,
  `time_id` int,
  `vote_count` int
);

ALTER TABLE `MovieRatings` ADD FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`);

ALTER TABLE `MovieRatings` ADD FOREIGN KEY (`time_id`) REFERENCES `Time` (`time_id`);

ALTER TABLE `PopularityFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`);

ALTER TABLE `PopularityFact` ADD FOREIGN KEY (`time_id`) REFERENCES `Time` (`time_id`);

ALTER TABLE `VotesFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`movie_id`);

ALTER TABLE `VotesFact` ADD FOREIGN KEY (`time_id`) REFERENCES `Time` (`time_id`);

ALTER TABLE `MovieRatings` ADD FOREIGN KEY (`movie_id`) REFERENCES `Director` (`director_id`);

ALTER TABLE `MovieRatings` ADD FOREIGN KEY (`movie_id`) REFERENCES `Genre` (`genre_id`);

ALTER TABLE `MovieRatings` ADD FOREIGN KEY (`movie_id`) REFERENCES `Cast` (`cast_id`);

ALTER TABLE `PopularityFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Director` (`director_id`);

ALTER TABLE `PopularityFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Genre` (`genre_id`);

ALTER TABLE `PopularityFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Cast` (`cast_id`);

ALTER TABLE `VotesFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Director` (`director_id`);

ALTER TABLE `VotesFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Genre` (`genre_id`);

ALTER TABLE `VotesFact` ADD FOREIGN KEY (`movie_id`) REFERENCES `Cast` (`cast_id`);
