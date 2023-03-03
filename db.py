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
    pool = ThreadedConnectionPool(1, 5, dsn=DATABASE_URL)


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


def add_photo(id,title, description, location, image_url, user_id):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding id %s", id)
        current_app.logger.info("Adding title %s", title)
        current_app.logger.info("Adding description %s", description)
        current_app.logger.info("Adding location %s", location)
        current_app.logger.info("Adding image_url %s", image_url)
        current_app.logger.info("Adding user_id %s", user_id)
        cur.execute("INSERT INTO photos (id, title, description, location, image_url, user_id) values (%s,%s,%s,%s,%s,%s)",
                    (id, title, description, location, image_url, user_id))


def get_photos():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM photos")
        return cur.fetchall()


def edit_photo(id, title, description, location, image_url):
    with get_db_cursor(True) as cur:
        cur.execute("UPDATE photos SET title = %s, description = %s, location = %s, image_url = %s WHERE id = %s",
                    (title, description, location, image_url, id))


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
        cur.execute(
            "INSERT INTO likes (user_id, photo_id) values (%s,%s)", (user_id, photo_id))


def get_likes_by_user_id(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM likes WHERE user_id = %s", (user_id))
        return cur.fetchall()


def get_likes_by_photo_id(photo_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM likes WHERE photo_id = %s", (photo_id))
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
        cur.execute(
            "INSERT INTO saved_photos (user_id, photo_id) values (%s,%s)", (user_id, photo_id))

# get all saved photos


def get_saved_photos(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM saved_photos WHERE user_id = %s", (user_id))
        return cur.fetchall()

# get a single saved photo


def get_saved_photo(user_id, photo_id):
    with get_db_cursor() as cur:
        cur.execute(
            "SELECT * FROM saved_photos WHERE user_id = %s AND photo_id = %s", (user_id, photo_id))
        return cur.fetchone()

# I think remove saved photos need two parameters to work properly


def remove_saved_photos(user_id, photo_id):
    with get_db_cursor(True) as cur:
        cur.execute(
            "DELETE FROM saved_photos WHERE user_id = %s AND photo_id = %s", (user_id, photo_id))

##############################
# Users
##############################


def get_user_by_id(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM username WHERE id = %s", (user_id))
        return cur.fetchone()


# create users using auth0 token information(name, email, profileurl), if user already exists, update
def create_user(name, email, profile_url):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO users (username, email, profile_pic_url) values (%s,%s,%s)", (name, email, profile_url))


def get_user_by_name(name):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (name))
        return cur.fetchone()


def get_all_users():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()


def delete_user(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM users WHERE id = %s", (id))


def edit_user(id, name, email, profile_pic_url):
    with get_db_cursor(True) as cur:
        cur.execute("UPDATE users SET username = %s, email = %s, profile_pic_url = %s WHERE id = %s",
                    (name, email, profile_pic_url, id))


##############################
# Comments
##############################


def create_comment(user_id, photo_id, comment):
    with get_db_cursor(True) as cur:
        cur.execute("INSERT INTO comments (user_id, photo_id, comment) values (%s,%s,%s)",
                    (user_id, photo_id, comment))
        return cur.fetchone()


def get_comments_by_photo_id(photo_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM comments WHERE photo_id = %s", (photo_id))
        return cur.fetchall()


def get_comments_by_user_id(user_id):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM comments WHERE user_id = %s", (user_id))
        return cur.fetchall()


def delete_comment(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM comments WHERE id = %s", (id))


def update_comment(id, comment):
    with get_db_cursor(True) as cur:
        cur.execute(
            "UPDATE comments SET comment = %s WHERE id = %s", (comment, id))

##############################
# Search
##############################


def search_photos(search_term):
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM photos WHERE title LIKE %s OR description LIKE %s OR location LIKE %s",
                    (search_term, search_term, search_term))
        return cur.fetchall()
