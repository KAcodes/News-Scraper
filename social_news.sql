DROP DATABASE IF EXISTS news;
CREATE DATABASE news;

DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS stories;

CREATE TABLE stories (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT NOT NULL,
  created_at timestamp NOT NULL,
  updated_at timestamp NOT NULL
);


CREATE TABLE votes (
     id serial PRIMARY KEY,
     direction TEXT NOT NULL,
     created_at timestamp NOT NULL,
     updated_at timestamp NOT NULL,
     story_id INT
  );

ALTER TABLE votes ADD CONSTRAINT story_fk FOREIGN KEY(story_id) REFERENCES stories(id);
