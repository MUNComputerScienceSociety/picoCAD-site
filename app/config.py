import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", True)
SECRET_KEY = os.getenv("PICOCAD_SITE_SECRET_KEY", "abc123")
GITHUB_CLIENT_ID = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_ID", None)
GITHUB_CLIENT_SECRET = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_SECRET", None)
GITHUB_REDIRECT_URI = os.getenv("PICOCAD_SITE_GITHUB_REDIRECT_URI", "http://localhost:8000/auth/github")
ADMIN_GITHUB_USERNAMES = os.getenv(
    "PICOCAD_SITE_ADMIN_GITHUB_USERNAMES", "jackharrhy,dchicasduena"
).split(",")
