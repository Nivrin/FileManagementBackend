from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint

from app.database.database import get_db
from app.models.group import Group
from app.models.user import User
from app.schemas.group import GroupCreate, GroupResponse
router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/CreateGroup/", response_model=GroupResponse, description="Create a new group")
def create_user(group: GroupCreate, db: Session = Depends(get_db)):
    """
    Create a new user group.

    Args:
        group (GroupCreate): The details of the group to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        GroupResponse: The details of the created group.
    """
    try:
        db_group = Group(**group.dict())
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


@router.get("/GetAllGroups/", response_model=List[GroupResponse], description="Get all groups")
def get_all_groups(db: Session = Depends(get_db)):
    """
    Retrieve all user groups.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[GroupResponse]: A list of all user groups.
    """
    try:
        groups = db.query(Group).all()
        return groups
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


@router.get("/GetGroupByID/", response_model=GroupResponse, description="Get group by ID")
def get_group_by_id(group_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Retrieve a user group by its ID.

    Args:
        group_id (int): The ID of the group to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        GroupResponse: The details of the requested group.

    Raises:
        HTTPException: If the group with the specified ID is not found or an error occurs.
    """
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return group
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


@router.post("/ShareUserWithGroup/{file_id}", response_model=GroupResponse, description="Share file with a user.")
def share_file_with_group(user_id: conint(ge=1), group_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Share a user with a group.

    Args:
        user_id (int): The ID of the user to share.
        group_id (int): The ID of the group to share the group with.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FileResponse: The details of the Group after sharing.

    Raises:
        HTTPException: If the user or group with the specified IDs are not found, or if an error occurs.
    """
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user in group.users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already shared with this group")

        group.users.append(user)
        db.commit()
        db.refresh(group)

        return group

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))