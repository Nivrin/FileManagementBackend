from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import (POSTGRES_USER, POSTGRES_PASSWORD,
                               POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                           f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
