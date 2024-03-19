from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.file import File
from app.models.user import User
from app.models.group import Group
from app.schemas.file import FileCreate


async def create_file_db(file: FileCreate, db: Session):
    try:
        db_file = File(**file.dict())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_file

    except Exception as e:
        db.rollback()
        raise e


async def get_files_db(db: Session):
    try:
        files = db.query(File).all()

        return files

    except Exception as e:
        raise e


async def get_file_by_id_db(file_id: int, db: Session):
    try:
        file = db.query(File).filter(File.id == file_id).first()

        if file is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        return file

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise e


async def share_file_with_user_db(file_id: int, user_id: int, db: Session):
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

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise e


async def share_file_with_group_db(file_id: int, group_id: int, db: Session):
    try:
        file = db.query(File).filter(File.id == file_id).first()
        group = db.query(Group).filter(Group.id == group_id).first()

        if file is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

        if group in file.groups:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is already shared with this group")

        file.users.append(group)
        db.commit()
        db.refresh(file)

        return file

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise e
