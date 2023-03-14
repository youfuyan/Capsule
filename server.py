# flask blueprint
# Make a decorator if user is logged in or not -> write function
# Making sure people who didnt login cant do function

from flask import *
import json
from os import environ as env
import base64
from urllib.parse import quote_plus, urlencode, quote
import db
from api import api

from authlib.integrations.flask_client import OAuth
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


app.register_blueprint(api)


@app.before_first_request
def initialize():
    db.setup()


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# AUTH0
# connection = http.client.HTTPSConnection(env.get("AUTH0_DOMAIN"))
# payload = "{\"client_id\":\"" + env.get("AUTH0_CLIENT_ID") + "\",\"client_secret\":\"" + env.get("AUTH0_CLIENT_SECRET") + "\",\"audience\":\"https://" + env.get("AUTH0_DOMAIN") + "/api/v2/\",\"grant_type\":\"client_credentials\"}"
# headers = { 'content-type': "application/json" }
# connection.request("POST", "/oauth/token", payload, headers)

# res = connection.getresponse()
# data = res.read()
# data_json = json.loads(data)
# auth_access_token = data_json['access_token']
# access_token = data.decode("utf-8").access_token


@app.route("/login")
def login():
    # return a flask object redirecting a html
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    tokenStr = json.loads(json.dumps(session.get('user')))

    user_id = tokenStr["userinfo"]["sub"]
    name = tokenStr["userinfo"]["nickname"]
    email = tokenStr["userinfo"]["email"]
    profile_pic_url = tokenStr["userinfo"]["picture"]
    userExists = db.get_user_by_id(str(user_id))

    if not userExists:
        db.create_user(user_id, name, email, profile_pic_url)

    return redirect("/gallery")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("header", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


imagekit = ImageKit(
    private_key=env.get("IMAGEKIT_PRIVATE_KEY"),
    public_key=env.get("IMAGEKIT_PUBLIC_KEY"),
    url_endpoint=env.get("IMAGEKIT_URL_ENDPOINT")
)


@app.route("/")
def header():
    return render_template('login.html')


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template('sideBar.html')


@app.route("/sideBar", methods=["GET", "POST"])
def sideBar():
    return render_template('responsiveSideBar.html')


@app.route("/comments/<id>", methods=["GET", "POST"])
def comments(id):
    getSession = session.get('user')
    if getSession:
        # for submitting the new comment
        if request.method == 'POST':
            tokenStr = json.loads(json.dumps(session.get('user')))
            # get current session's/logged in user's username
            user_id = tokenStr["userinfo"]["sub"]
            photo_id = id
            newComment = request.form['comment']
            # print(newComment)
            db.create_comment(user_id, photo_id, newComment)
            return redirect(url_for('comments', id=id))
            # return render_template('comments.html', session=getSession, comments=allComments)

        # for get request
        else:
            allComments = db.get_comments_by_photo_id(id)
            commentsJson = []
            for comment in allComments:
                userId = comment["user_id"]
                userName = db.get_user_by_id(userId)[1]
                photo_url = db.get_user_by_id(userId)[3]
                commentsJson.append({"id": comment[0], "comment": comment[1],
                                     "user_name": userName, "photo_id": comment[3], "timestamp": comment[4], "photo_url": photo_url})

            return render_template('comments.html', session=getSession, comments=commentsJson)
    else:
        return redirect(url_for('header'))


@app.route("/addPost", methods=["GET", "POST"])
def addPost():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]

        if request.method == 'POST':
            # Get the form data
            title = request.form['title']
            body = request.form['body']
            location = request.form['location']
            photo = request.files['image']

            photo_string = base64.b64encode(photo.read())
            photo_name = secure_filename(photo.filename)

            upload = imagekit.upload(file=photo_string,
                                     file_name=photo_name,
                                     options=UploadFileRequestOptions())
            # print(upload.file_id)
            # print(upload.url)

            # Do something with the form data (e.g. save to a database)
            db.add_photo(upload.file_id, title, body,
                         location, upload.url, user_id)

            return redirect(url_for('galleryPage'))

        return render_template('addPost.html', session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/deletePost", methods=["POST"])
def deletePost():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]

        if request.method == 'POST':
            # Get the form data
            photo_id = request.form['photo_id']
            photo = db.get_photo_by_image_id(photo_id)
            if user_id == photo["user_id"]:
                imagekit.delete_file(file_id=photo_id)
                db.delete_photo(photo_id)

            return redirect(url_for('profile'))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]
        photos = db.get_photos_by_user_id(user_id)
        personal_likes = db.get_likes_by_user_id(user_id)

        posts_count = len(photos)
        personal_likes_count = len(personal_likes)

        return render_template('profile.html', photos=photos, session=getSession,
                               posts_count=posts_count, personal_likes_count=personal_likes_count)
    else:
        return redirect(url_for('header'))


@app.route("/liked", methods=["GET", "POST"])
def liked():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]
        posts = db.get_photos_by_user_id(user_id)
        personal_likes = db.get_likes_by_user_id(user_id)

        posts_count = len(posts)
        personal_likes_count = len(personal_likes)

        photos = []
        for personal_like in personal_likes:
            photo = db.get_photo_by_image_id(personal_like["photo_id"])
            photos.append(photo)

        return render_template('profile.html', photos=photos, personal_likes=personal_likes, session=getSession,
                               posts_count=posts_count, personal_likes_count=personal_likes_count)
    else:
        return redirect(url_for('header'))


@app.route("/editPost", methods=["GET", "POST"])
def editProfile():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]
        print(user_id)
        if request.method == 'POST':
            id = request.form['photo_id']
            title = request.form['title']
            body = request.form['body']
            location = request.form['location']
            image = request.form['image']
            print(id, title, body, location, image)
            db.edit_photo(id, title, body, location, image)
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            photo_id = request.args.get('photo_id')
            photo = db.get_photo_by_image_id(photo_id)
            # security reason if not owner redirect to profile
            if user_id == photo["user_id"]:
                return render_template('editPost.html', photo=photo, session=getSession)
            else:
                return redirect(url_for('profile'))
    else:
        return redirect(url_for('header'))


@app.route("/search", methods=["GET", "POST"])
def search():
    getSession = session.get('user')
    if getSession:
        if request.method == 'POST':
            query = request.form['query']
            photos = db.search_photos(query)
            tokenStr = json.loads(json.dumps(session.get('user')))
            sessionStr = tokenStr["userinfo"]
            return render_template('search.html', session=sessionStr, photos=photos, query=query)
        else:
            return render_template('search.html', session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/gallery", methods=["GET", "POST"])
def galleryPage():
    getSession = session.get('user')
    allPhotos = db.get_photos()
    print(len(allPhotos))
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        sessionStr = tokenStr["userinfo"]
        return render_template('gallery.html', session=sessionStr, photos=allPhotos)
    else:
        return render_template('gallery.html', photos=allPhotos)


@app.route("/loginPage", methods=["GET", "POST"])
def loginPage():
    return render_template('login.html')


@app.route("/signUpPage", methods=["GET", "POST"])
def signUpPage():
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
