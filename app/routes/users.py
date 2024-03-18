from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import User, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/GetAllUsers/", response_model=List[UserResponse], description="get all users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/GetUserByID/", response_model=UserResponse, description="get user by id.")
def get_users_by_id(user_id: conint(ge=1), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    return user


@router.get("/GetUserByName/", response_model=UserResponse, description="get user by name.")
def get_users_by_name(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    return user
