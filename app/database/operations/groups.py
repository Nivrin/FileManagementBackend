from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.group import Group
from app.models.user import User
from app.schemas.group import GroupCreate


async def create_group_db(group: GroupCreate, db: Session):
    try:
        db_group = Group(**group.dict())
        db.add(db_group)
        db.commit()
        db.refresh(db_group)

        return db_group

    except Exception as e:
        db.rollback()
        raise e


async def get_all_groups_db(db: Session):
    try:
        groups = db.query(Group).all()

        return groups

    except Exception as e:
        raise e


async def get_group_by_id_db(group_id: int, db: Session):
    try:
        group = db.query(Group).filter(Group.id == group_id).first()

        return group

    except Exception as e:
        raise e


async def share_group_with_user_db(group_id: int, user_id: int, db: Session):
    try:
        group = db.query(Group).filter(Group.id == group_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user in group.users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group is already shared with this user")

        group.users.append(user)
        db.commit()
        db.refresh(group)

        return group

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        db.rollback()
        raise e
