from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlmodel import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth

import config
from db import User, engine

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

templates = Jinja2Templates(directory="templates")

oauth = OAuth()
oauth.register(
    name="github",
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


@app.get("/login/github")
async def login_via_github(request: Request):
    redirect_uri = request.url_for("auth_via_github")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@app.get("/auth/github")
async def auth_via_github(request: Request) -> User:
    token = await oauth.github.authorize_access_token(request)
    data = (await oauth.github.get("user", token=token)).json()

    github_username = data["login"]

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.github_username == github_username)
        ).first()

        if user is None:
            user = User(github_username=github_username)
            session.add(user)

        request.session["github_username"] = github_username

        session.commit()

        return RedirectResponse(url="/")


@app.get("/api/")
async def root():
    return {"timestamp": datetime.now().isoformat()}


@app.get("/")
async def index(request: Request):
    github_username = request.session.get("github_username", None)

    return templates.TemplateResponse(
        "index.jinja", {"request": request, "github_username": github_username}
    )
