import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint

from app.database.database import get_db
from app.schemas.group import GroupCreate, GroupResponse
from app.database.operations.groups import (create_group_db, get_all_groups_db,
                                            get_group_by_id_db, share_group_with_user_db)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("/CreateGroup/", response_model=GroupResponse, description="Create a new group")
async def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """
    Create a new user group.

    Args:
        group (GroupCreate): The details of the group to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        GroupResponse: The details of the created group.
    """
    try:
        created_group: GroupResponse = await create_group_db(group, db)

        logger.info(f"Group- '{group.name}' created.")
        return created_group

    except Exception as e:
        logger.error(f"Error occurred while creating group: '{group.name}' - {e}")
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating a group")


@router.get("/GetAllGroups/", response_model=List[GroupResponse], description="Get all groups")
async def get_all_groups(db: Session = Depends(get_db)):
    """
    Retrieve all user groups.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[GroupResponse]: A list of all user groups.
    """
    try:
        groups_retrieved: List[GroupResponse] = await get_all_groups_db(db)

        logger.info(f"All groups retrieved.")
        return groups_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving all groups - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving groups")


@router.get("/GetGroupByID/", response_model=GroupResponse, description="Get group by ID")
async def get_group_by_id(group_id: conint(ge=1), db: Session = Depends(get_db)):
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
        group_retrieved: GroupResponse = await get_group_by_id_db(group_id, db)

        logger.info(f"Group: '{group_retrieved.name}' - retrieved.")
        return group_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving group with id: {group_id} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving a group")


@router.post("/ShareUserWithGroup/{file_id}", response_model=GroupResponse, description="Share file with a user.")
async def share_group_with_user(group_id: conint(ge=1), user_id: conint(ge=1), db: Session = Depends(get_db)):
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
        group_shared: GroupResponse = await share_group_with_user_db(group_id, user_id, db)

        logger.info(f"Group: '{group_shared.name}' shared with user.")
        return group_shared

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error occurred while sharing group with id: '{group_id}' with user with id: '{user_id}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while sharing a group with user")
