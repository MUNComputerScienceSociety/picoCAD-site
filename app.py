import os

from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", True)
SECRET_KEY = os.getenv("PICOCAD_SITE_SECRET_KEY", "abc123")
GITHUB_CLIENT_ID = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_ID", None)
GITHUB_CLIENT_SECRET = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_SECRET", None)

if DEBUG:
    print("WARNING: Running in debug mode, since DEBUG is true")

    print("WARNING: Permitting insecure transports in oauthlib, since DEBUG is true")
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if GITHUB_CLIENT_ID is None or GITHUB_CLIENT_SECRET is None:
    raise "GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set in .env"

app = Flask(__name__)
app.secret_key = SECRET_KEY
blueprint = make_github_blueprint(
    client_id=GITHUB_CLIENT_ID, client_secret=GITHUB_CLIENT_SECRET
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    assert resp.ok

    return "You are @{login} on GitHub".format(login=resp.json()["login"])
