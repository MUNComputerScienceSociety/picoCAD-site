from sqlmodel import Field, SQLModel, create_engine

from app.config import DEBUG


class User(SQLModel, table=True):
    github_username: str = Field(primary_key=True)
    admin: bool = Field(default=False)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=DEBUG)

SQLModel.metadata.create_all(engine)
