CREATE TABLE users (
  id VARCHAR(256) PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  profile_pic_url VARCHAR(2048) NOT NULL,
  saved_photos TEXT[]
);

CREATE TABLE photos (
  id VARCHAR(100) PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  location VARCHAR(100),
  upload_date TIMESTAMP NOT NULL DEFAULT NOW(),
  image_url VARCHAR(2048) NOT NULL,
  user_id VARCHAR(256) NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(256) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  photo_id VARCHAR(100) NOT NULL REFERENCES photos(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE comments (
  id SERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  user_id VARCHAR(256) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  photo_id VARCHAR(100) NOT NULL REFERENCES photos(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE saved_photos (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(256) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  photo_id VARCHAR(100) NOT NULL REFERENCES photos(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- CREATE INDEX idx_photos_search ON photos USING gin(to_tsvector('english', title || ' ' || description));
-- CREATE INDEX title_idx ON photos USING gin (title gin_trgm_ops);
-- CREATE INDEX description_idx ON photos USING gin (description gin_trgm_ops);
CREATE INDEX title_idx ON photos USING gin (title gin_trgm_ops);
CREATE INDEX description_idx ON photos USING gin (description gin_trgm_ops);
CREATE INDEX title_tsv_idx ON photos USING gin (to_tsvector('english', title));
CREATE INDEX description_tsv_idx ON photos USING gin (to_tsvector('english', description));


CREATE EXTENSION pg_trgm;
