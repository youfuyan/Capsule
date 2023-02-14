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

## AUTH0
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
    # session['sid'] = token['user_info']['sid']
    # session['email'] = token['user_info']['email']
    # session['picture'] = token['user_info']['picture']
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


#  the root page describes the survey and asks the user to consent to participate. 
# It has two buttons at the bottom: “consent” (go to /survey) and “decline” (go to /decline).
@app.route("/")
def index():
  return render_template('index.html')


@app.route("/main")
def main():
  return render_template('main.html')


# /survey
# asks the user a few questions, then a “next” button (go to /thanks). The input types must include:
# text input – this field is “required” and has a minimum length of 3 characters. The user cannot proceed without filling it out – use html5 validation.
# a group of 3 or more radio buttons
# select box with 3 or more options
# checkbox
# finally, there must be one “conditional” field of type textarea that appears or disappears depending on the state of the checkbox input.
@app.route('/survey', methods=['GET'])
def survey():
  return render_template('survey.html')


# /decline - a page that says “thanks anyway” or something like that
@app.route('/decline', methods=['GET'])
def decline():
  return render_template('decline.html')


# /thanks - says thank you to the user for completing the survey
@app.route('/thanks', methods=['GET'])
def thanks():
  return render_template('thanks.html')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
