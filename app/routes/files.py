from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint
from sqlalchemy import func

from app.database.database import get_db
from app.models.file import File
from app.schemas.file import FileCreate, FileResponse
from app.models.user import User
from app.models.group import Group


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/CreateFile/", response_model=FileResponse, description="Create file.")
def create_file(file: FileCreate, db: Session = Depends(get_db)):
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
        db_file = File(**file.dict())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


@router.get("/GetAllFiles/", response_model=List[FileResponse], description="Get all files.")
def get_files(db: Session = Depends(get_db)):
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
        files = db.query(File).all()
        return files
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred")


@router.get("/GetFileByID/", response_model=FileResponse, description="Get file by ID.")
def get_file_by_id(file_id: conint(ge=1), db: Session = Depends(get_db)):
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
        file = db.query(File).filter(File.id == file_id).first()
        if file is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return file
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @router.get("/TopSharedFiles/", response_model=List[FileResponse], description="Get top shared files.")
# def get_top_shared_files(k: conint(ge=1, le=10), db: Session = Depends(get_db)):
#     top_shared_files = db.query(
#         File.id, File.name, File.risk,
#         func.count(User.id).label('user_count')) \
#         .join(User, File.users) \
#         .group_by(File.id) \
#         .order_by(func.count(User.id).desc()) \
#         .limit(k) \
#         .all()
#
#     return db_file


@router.post("/ShareFileWithUser/{file_id}", response_model=FileResponse, description="Share file with a user.")
def share_file_with_group(file_id: conint(ge=1), user_id: conint(ge=1), db: Session = Depends(get_db)):
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
        file = db.query(File).filter(File.id == file_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        if file is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user in file.users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is already shared with this user")

        file.users.append(user)
        db.commit()
        db.refresh(file)

        return file

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/ShareFileWithGroup/{file_id}", response_model=FileResponse, description="Share file with a user.")
def share_file_with_group(file_id: conint(ge=1), group_id: conint(ge=1), db: Session = Depends(get_db)):
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
        file = db.query(File).filter(File.id == file_id).first()
        user = db.query(Group).filter(Group.id == group_id).first()

        if file is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

        if user in file.groups:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is already shared with this group")

        file.groups.append(user)
        db.commit()
        db.refresh(file)

        return file

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))