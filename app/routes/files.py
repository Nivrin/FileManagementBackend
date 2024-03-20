import logging
from pydantic import conint
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.operations.files import (create_file_db, get_files_db,
                                           get_file_by_id_db, share_file_with_user_db,
                                           share_file_with_group_db, get_top_shared_file_db)
from app.schemas.file import FileCreate, FileResponse, FileTopSharedResponse


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/CreateFile/", response_model=FileResponse, description="Create file.")
async def create_file(file: FileCreate, db: Session = Depends(get_db)):
    """
    Create a new file.

    Args:
        file (FileCreate): The details of the file to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FileResponse: The details of the created file.

    Raises:
        HTTPException: If an error occurs during the creation process.
    """
    try:
        file_created: FileResponse = await create_file_db(file, db)

        logger.info(f"File: '{file.name}' - created.")
        return file_created

    except Exception as e:
        logger.error(f"Error occurred during the creation of file- '{file.name}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating a file"
        )


@router.get("/GetAllFiles/", response_model=List[FileResponse], description="Get all files.")
async def get_files(db: Session = Depends(get_db)):
    """
    Retrieve all files.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[FileResponse]: A list of all files.

    Raises:
        HTTPException: If an error occurs during the retrieval process.
    """
    try:
        files_retrieved: List[FileResponse] = await get_files_db(db)

        logger.info(f"All Files retrieved.")
        return files_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving files: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving files"
        )


@router.get("/GetFileByID/{file_id}", response_model=FileResponse, description="Get file by ID.")
async def get_file_by_id(file_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Retrieve a file by its ID.

    Args:
        file_id (int): The ID of the file to retrieve.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FileResponse: The details of the requested file.

    Raises:
        HTTPException: If the file with the specified ID is not found or an error occurs.
    """
    try:
        file_retrieved: FileResponse = await get_file_by_id_db(file_id, db)

        logger.info(f"File: '{file_retrieved.name}' - retrieved to user.")
        return file_retrieved

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error occurred while retrieving file with id: '{file_id}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving a file"
        )


@router.post("/ShareFileWithUser/", response_model=FileResponse, description="Share file with a user.")
async def share_file_with_user(file_id: conint(ge=1), user_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Share a file with a group.

    Args:
        file_id (int): The ID of the file to share.
        user_id (int): The ID of the user to share the file with.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FileResponse: The details of the file after sharing.

    Raises:
        HTTPException: If the file or user with the specified IDs are not found, or if an error occurs.
    """
    try:
        file_shared: FileResponse = await share_file_with_user_db(file_id, user_id, db)

        logger.info(f"File: '{file_shared.name}' shared with user.")
        return file_shared

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        logger.error(f"Error occurred while sharing file with id: '{file_id}' with user with id: '{user_id}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while sharing a file with a user"
        )


@router.post("/ShareFileWithGroup/", response_model=FileResponse, description="Share file with a group.")
async def share_file_with_group(file_id: conint(ge=1), group_id: conint(ge=1), db: Session = Depends(get_db)):
    """
    Share a file with a group.

    Args:
        file_id (int): The ID of the file to share.
        group_id (int): The ID of the group to share the file with.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        FileResponse: The details of the file after sharing.

    Raises:
        HTTPException: If the file or group with the specified IDs are not found, or if an error occurs.
    """
    try:
        file_shared: FileResponse = await share_file_with_group_db(file_id, group_id, db)

        logger.info(f"File- '{file_shared.name}' shared with a group.")
        return file_shared

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error occurred while sharing file with id: '{file_id}' with group with id: '{group_id}' - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while sharing a file with a group."
        )


@router.get("/TopSharedFiles/{k}", response_model=List[FileTopSharedResponse], description="Get top shared files.")
async def get_top_shared_files(k:  conint(ge=1, le=10) = 5, db: Session = Depends(get_db)):
    """
    Retrieve the top shared files.

    Args:
        k (int): The number of top shared files to retrieve. Default is 5.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[FileTopSharedResponse]: A list of FileTopSharedResponse objects representing the top shared files.

    Raises:
        HTTPException: If an error occurs during the retrieval process.
    """
    try:
        files_retrieved: List[FileTopSharedResponse] = await get_top_shared_file_db(k, db)

        logger.info(f"Top {k} shared files retrieved.")
        return files_retrieved

    except Exception as e:
        logger.error(f"Error occurred while retrieving {k} top shared files - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving top shared files."
        )
