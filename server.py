from flask import *
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth


app = Flask(__name__)

app.secret_key = env.get("FLASK_SECRET")

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
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# @app.before_first_request
# def initialize():
#     db.setup()


@app.route("/")
def header():
  return render_template('profile.html')


@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/sideBar", methods=["GET", "POST"])
def sideBar():
    return render_template('sideBar.html')


@app.route("/comments", methods=["GET", "POST"])
def comments():
    return render_template('comments.html')


@app.route("/addPost", methods=["GET", "POST"])
def addPost():
    return render_template('addPost.html')
    #   if request.method == 'POST':
    #     # Get the form data
    #     title = request.form['title']
    #     body = request.form['body']
    #     location = request.form['location']
    #     photo = request.files.get('photo')
    #     is_draft = request.form.get('draft') == 'on'

    #     # Save the photo to disk
    #     if photo:
    #         filename = photo.filename
    #         photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #     # Do something with the form data (e.g. save to a database)
    #     # ...

    #     return redirect(url_for('home'))

    # return render_template('add_post.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
  return render_template('profile.html')

@app.route("/editProfile", methods=["GET", "POST"])
def editProfile():
  return render_template('editProfile.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
