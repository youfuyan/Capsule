from flask import *
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
import db

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
    return render_template('login.html')


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


@app.route("/loginPage", methods=["GET", "POST"])
def loginPage():
    return render_template('login.html')


@app.route("/signUpPage", methods=["GET", "POST"])
def signUpPage():
    return render_template('signUp.html')

#######################
# API
#######################

# Photos


@app.route("/api/photos/get", methods=['GET'])
def getPhotosAPI():
    photos = db.get_photos()

    json = []
    for photo in photos:
        json.append({"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
                    "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]})

    return jsonify(json)


@app.route("/api/photos/get/<id>", methods=['GET'])
def getPhotoAPI(id):
    photo = db.get_photos(id)
    json = {"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
            "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]}
    return jsonify(json)


@app.route("/api/photos/add", methods=['POST'])
def addPhotoAPI():
    data = request.get_json()
    db.add_photo(data['title'], data['description'], data['location'],
                 data['upload_date'], data['image_url'], data['user_id'])
    return jsonify({"success": True})


@app.route("/api/photos/delete/<id>", methods=['DELETE'])
def deletePhotoAPI(id):
    db.delete_photo(id)
    return jsonify({"success": True})


@app.route("/api/photos/edit/<id>", methods=['PUT'])
def editPhotoAPI(id):
    data = request.get_json()
    db.edit_photo(id, data['title'], data['description'], data['location'],
                  data['upload_date'], data['image_url'], data['user_id'])
    return jsonify({"success": True})

# Users


@app.route("/api/users/get_all", methods=['GET'])
def getAllUsersAPI():
    users = db.get_all_users()
    json = {"id": users[0], "username": users[1], "email": users[2],
            "profile_pic": users[3], "saved_photos": users[4]}
    return jsonify(json)


@app.route("/api/users/get/<id>", methods=['GET'])
def getUserAPI(id):
    user = db.get_user_by_id(id)
    json = {"id": user[0], "username": user[1], "email": user[2],
            "profile_pic": user[3], "saved_photos": user[4]}
    return jsonify(json)


@app.route("/api/users/get_by_username/<username>", methods=['GET'])
def getUserByUsernameAPI(username):
    user = db.get_user_by_name(username)
    json = {"id": user[0], "username": user[1], "email": user[2],
            "profile_pic": user[3], "saved_photos": user[4]}
    return jsonify(json)


@app.route("/api/users/create", methods=['POST'])
def createUserAPI():
    data = request.get_json()
    db.create_user(data['username'], data['email'], data['profile_pic'])
    return jsonify({"success": True})


@app.route("/api/users/delete/<id>", methods=['DELETE'])
def deleteUserAPI(id):
    db.delete_user(id)
    return jsonify({"success": True})


@app.route("/api/users/edit/<id>", methods=['PUT'])
def editUserAPI(id):
    data = request.get_json()
    db.edit_user(data['username'], data['email'], data['profile_pic'], id)
    return jsonify({"success": True})

# Saved Photos


@app.route("/api/users/add_save_photo/<user_id>/<photo_id>", methods=['PUT'])
def addSavePhotoAPI(user_id, photo_id):
    db.add_saved_photos(user_id, photo_id)
    return jsonify({"success": True})


@app.route("/api/users/remove_saved_photo/<user_id>/<photo_id>", methods=['DELETE'])
def removeSavedPhotoAPI(user_id, photo_id):
    db.remove_saved_photos(user_id, photo_id)
    return jsonify({"success": True})


@app.route("/api/users/get_saved_photos/<user_id>", methods=['GET'])
def getSavedPhotosAPI(user_id):
    photos = db.get_saved_photos(user_id)
    json = []
    for photo in photos:
        json.append({"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
                    "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]})
    return jsonify(json)


@app.route("/api/users/get_saved_photos/<user_id>/<photo_id>", methods=['GET'])
def getSavedPhotoAPI(user_id, photo_id):
    photo = db.get_saved_photo(user_id, photo_id)
    json = {"id": photo[0], "title": photo[1], "description": photo[2], "location": photo[3],
            "upload_date": photo[4], "image_url": photo[5], "user_id": photo[6]}
    return jsonify(json)

# Comments


@app.route("/api/comments/create", methods=['POST'])
def createCommentAPI():
    data = request.get_json()
    db.create_comment(data['user_id'], data['photo_id'], data['comment'])
    return jsonify({"success": True})


@app.route("/api/comments/get/<photo_id>", methods=['GET'])
def getCommentsbyPhotoIdAPI(photo_id):
    comments = db.get_comments_by_photo_id(photo_id)
    json = []
    for comment in comments:
        json.append({"id": comment[0], "comment": comment[1],
                    "user_id": comment[2], "photo_id": comment[3], })
    return jsonify(json)


@app.route("/api/comments/get/<user_id>", methods=['GET'])
def getCommentsbyUserIdAPI(user_id):
    comments = db.get_comments_by_user_id(user_id)
    json = []
    for comment in comments:
        json.append({"id": comment[0], "comment": comment[1],
                    "user_id": comment[2], "photo_id": comment[3], })
    return jsonify(json)


@app.route("/api/comments/delete/<id>", methods=['DELETE'])
def deleteCommentAPI(id):
    db.delete_comment(id)
    return jsonify({"success": True})


@app.route("/api/comments/edit/<id>", methods=['PUT'])
def editCommentAPI(id):
    data = request.get_json()
    db.edit_comment(id, data['comment'])
    return jsonify({"success": True})

# Likes


@app.route("/api/likes/create", methods=['POST'])
def createLikeAPI():
    data = request.get_json()
    db.add_like(data['user_id'], data['photo_id'])
    return jsonify({"success": True})


@app.route("/api/likes/get/<photo_id>", methods=['GET'])
def getLikesbyPhotoIdAPI(photo_id):
    likes = db.get_likes_by_photo_id(photo_id)
    json = []
    for like in likes:
        json.append({"id": like[0], "user_id": like[1], "photo_id": like[2]})
    return jsonify(json)


@app.route("/api/likes/get/<user_id>", methods=['GET'])
def getLikesbyUserIdAPI(user_id):
    likes = db.get_likes_by_user_id(user_id)
    json = []
    for like in likes:
        json.append({"id": like[0], "user_id": like[1], "photo_id": like[2]})
    return jsonify(json)


@app.route("/api/likes/delete/<id>", methods=['DELETE'])
def deleteLikeAPI(id):
    db.remove_like(id)
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
