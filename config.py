import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", True)
SECRET_KEY = os.getenv("PICOCAD_SITE_SECRET_KEY", "abc123")
GITHUB_CLIENT_ID = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_ID", None)
GITHUB_CLIENT_SECRET = os.getenv("PICOCAD_SITE_GITHUB_CLIENT_SECRET", None)
