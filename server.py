# flask blueprint
# Make a decorator if user is logged in or not -> write function
# Making sure people who didnt login cant do function

from flask import *
import json
from os import environ as env
import base64
from urllib.parse import quote_plus, urlencode
import db
import api

from authlib.integrations.flask_client import OAuth
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")


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


@app.route("/comments", methods=["GET", "POST"])
def comments():
    getSession = session.get('user')
    if getSession:
        return render_template('comments.html', session=getSession)
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
            is_draft = request.form.get('draft') == 'on'

            photo_string = base64.b64encode(photo.read())
            photo_name = secure_filename(photo.filename)

            upload = imagekit.upload(file=photo_string,
                                     file_name=photo_name,
                                     options=UploadFileRequestOptions())
            print(upload.file_id)
            print(upload.url)

            # Do something with the form data (e.g. save to a database)
            db.add_photo(upload.file_id, title, body,
                         location, upload.url, user_id)

            return redirect(url_for('galleryPage'))

        return render_template('addPost.html', session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    getSession = session.get('user')
    if getSession:
        tokenStr = json.loads(json.dumps(session.get('user')))
        user_id = tokenStr["userinfo"]["sub"]
        photos = db.get_photos_by_user_id(user_id)

        return render_template('profile.html', photos=photos, session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/editProfile", methods=["GET", "POST"])
def editProfile():
    getSession = session.get('user')
    if getSession:
        if request.method == 'POST':
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            return render_template('editProfile.html', session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/search", methods=["GET", "POST"])
def search():
    getSession = session.get('user')
    if getSession:
        if request.method == 'POST':
            query = request.form['query']
            photos = db.search_photos(query)
            return render_template('search.html', session=getSession, photos=photos, query=query)
        else:
            return render_template('search.html', session=getSession)
    else:
        return redirect(url_for('header'))


@app.route("/gallery", methods=["GET", "POST"])
def galleryPage():
    allPhotos = db.get_photos()
    return render_template('gallery.html', photos=allPhotos)


@app.route("/loginPage", methods=["GET", "POST"])
def loginPage():
    return render_template('login.html')


@app.route("/signUpPage", methods=["GET", "POST"])
def signUpPage():
    return render_template('signUp.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
