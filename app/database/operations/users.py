from fastapi import HTTPException, status
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


async def get_user_by_id_db(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise e
