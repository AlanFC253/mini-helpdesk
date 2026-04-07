from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://helpdesk:helpdesk@localhost:5432/minihelpdesk"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()