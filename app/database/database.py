from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.conifg.config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}"
                           f":{DATABASE_PORT}/{DATABASE_NAME}")

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
