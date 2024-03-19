import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import conint
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.database.operations.users import (create_user_db,
                                           get_all_users_db, get_user_by_id_db)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/CreateUser/", response_model=UserResponse, description="Create a new user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): The details of the user to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The details of the created user.

    Raises:
        HTTPException: If an error occurs during the creation process.
    """
    try:
        created_user: UserCreate = await create_user_db(user, db)

        logger.info(f"User- '{user.name}' created.")
        return created_user

    except Exception as e:
        logger.error(f"Error occurred while creating user: '{user.name}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating user"
        )


@router.get("/GetAllUsers/", response_model=List[UserResponse], description="Get all users")
async def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[UserResponse]: A list of all users.

    Raises:
        HTTPException: If an error occurs during the retrieval process.
    """
    try:
        users_retrieved: List[UserResponse] = await get_all_users_db(db)

        logger.info(f"All users retrieved.")
        return users_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving all users - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving users"
        )


@router.get("/GetUserByID/", response_model=UserResponse, description="Get user by ID")
async def get_user_by_id(user_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Retrieve a user by its ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        UserResponse: The details of the requested user.

    Raises:
        HTTPException: If the user with the specified ID is not found or an error occurs.
    """
    try:
        user_retrieved: UserResponse = await get_user_by_id_db(user_id, db)

        if user_retrieved is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        logger.info(f"User: '{user_retrieved.name}' - retrieved.")
        return user_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving user with id: '{user_id}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user"
        )