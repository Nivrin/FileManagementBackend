from pydantic import conint
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


async def create_user_db(user: UserCreate, db: Session):
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except Exception as e:
        db.rollback()
        raise e


async def get_all_users_db(db: Session):
    try:
        users = db.query(User).all()

        return users

    except Exception as e:
        raise e


async def get_user_by_id_db(user_id: conint(ge=1), db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        return user

    except Exception as e:
        raise e
