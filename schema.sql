CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  saved_photos TEXT[]
);

CREATE TABLE photos (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  location VARCHAR(100),
  upload_date TIMESTAMP NOT NULL DEFAULT NOW(),
  image_url VARCHAR(2048) NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id)
);

CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  photo_id INTEGER NOT NULL REFERENCES photos(id),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users(id),
  photo_id INTEGER NOT NULL REFERENCES photos(id),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE saved_photos (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  photo_id INTEGER NOT NULL REFERENCES photos(id),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
