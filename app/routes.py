from datetime import datetime

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.requests import Request
from sqlalchemy import select
from sqlmodel import Session

from app import config
from app.db import User, engine
from app.oauth import oauth

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


@router.get("/login/github")
async def login_via_github(request: Request):
    redirect_uri = request.url_for("auth_via_github")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/auth/github")
async def auth_via_github(request: Request) -> User:
    token = await oauth.github.authorize_access_token(request)
    data = (await oauth.github.get("user", token=token)).json()

    github_username = data["login"]

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.github_username == github_username)
        ).first()

        if user is None:
            is_admin = github_username in config.ADMIN_GITHUB_USERNAMES
            user = User(github_username=github_username, admin=is_admin)
            session.add(user)

        request.session["github_username"] = github_username

        session.commit()

        return RedirectResponse(url="/")


@router.get("/api/")
async def root():
    return {"timestamp": datetime.now().isoformat()}


@router.get("/")
async def index(request: Request):
    github_username = request.session.get("github_username", None)

    return templates.TemplateResponse(
        "index.jinja", {"request": request, "github_username": github_username}
    )
