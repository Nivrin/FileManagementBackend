from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.models.file import File
from app.models.user import User
from app.models.group import Group
from app.schemas.file import (FileCreate,
                              FileTopSharedResponse)


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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="File not found")

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="File not found")

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if user in file.users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File is already shared with this user")

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="File not found")

        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Group not found")

        if group in file.groups:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File is already shared with this group")

        file.groups.append(group)
        db.commit()
        db.refresh(file)

        return file

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise e


async def get_top_shared_file_db(k: int, db) -> List[FileTopSharedResponse]:
    try:
        top_shared_files_sql_query = text(f"""
        SELECT file_name,risk,
        COALESCE(string_agg(DISTINCT users, ',' )) AS merged_users,    
        COUNT(DISTINCT users) AS merged_users_count
        FROM
            (
            SELECT file_id,file_name,risk,users
            FROM (
                SELECT f.id AS file_id, f.name AS file_name,f.risk, u.name AS users
                FROM 
                    "file" AS f
                LEFT JOIN 
                    file_user AS fu ON f.id = fu.file_id
                LEFT JOIN 
                    "user" AS u ON fu.user_id = u.id

                UNION

                SELECT f.id AS file_id, f.name AS file_name,f.risk,ug_user.name AS users
                FROM 
                    "file" AS f
                LEFT JOIN 
                    file_group AS fg ON f.id = fg.file_id
                LEFT JOIN 
                    user_group AS ug ON fg.group_id = ug.group_id
                LEFT JOIN 
                    "user" AS ug_user ON ug.user_id = ug_user.id
            ) AS subquery)
        group by file_id, file_name,risk
        ORDER BY merged_users_count DESC
        LIMIT {k}
        """)

        result = db.execute(top_shared_files_sql_query)
        files = []
        for row in result:
            file_name, risk, merged_users, merged_users_count = row
            users: list[str] = merged_users.split(',') if merged_users else []
            file_data = {
                "name": file_name,
                "risk": risk,
                "users": users
            }
            files.append(FileTopSharedResponse(**file_data))
        return files

    except Exception as e:
        raise e
