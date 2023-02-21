""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 5, dsn=DATABASE_URL, sslmode='require')

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

##############################
# Photos
##############################

def add_photo(title, description, location, image_url, user_id):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding title %s", title)
        current_app.logger.info("Adding description %s", description)
        current_app.logger.info("Adding location %s", location)
        current_app.logger.info("Adding image_url %s", image_url)
        current_app.logger.info("Adding user_id %s", user_id)
        cur.execute("INSERT INTO photos (title, description, location, image_url, user_id) values (%s,%s,%s,%s,%s)", (title, description, location, image_url, user_id))

def get_photos():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM photos")
        return cur.fetchall()

def edit_photo(id, title, description, location, image_url):
    with get_db_cursor(True) as cur:
        cur.execute("UPDATE photos SET title = %s, description = %s, location = %s, image_url = %s WHERE id = %s", (title, description, location, image_url, id))

def delete_photo(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM photos WHERE id = %s", (id))

##############################
# Likes
##############################

def add_like(user_id, photo_id):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding user_id %s", user_id)
        current_app.logger.info("Adding photo_id %s", photo_id)
        cur.execute("INSERT INTO likes (user_id, photo_id) values (%s,%s)", (user_id, photo_id))

def get_likes(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM likes WHERE user_id = %s", (user_id))
        return cur.fetchall()

def remove_like(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM photos WHERE id = %s", (id))

##############################
# Saved Photos
##############################

def add_saved_photos(user_id, photo_id):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding user_id %s", user_id)
        current_app.logger.info("Adding photo_id %s", photo_id)
        cur.execute("INSERT INTO saved_photos (user_id, photo_id) values (%s,%s)", (user_id, photo_id))

def get_saved_photos(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM saved_photos WHERE user_id = %s", (user_id))
        return cur.fetchall()

def remove_saved_photos(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM saved_photos WHERE id = %s", (id))