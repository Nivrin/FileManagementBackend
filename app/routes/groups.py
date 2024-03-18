from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import conint

from app.database.database import get_db
from app.models.group import Group
from app.schemas.group import Group, GroupResponse

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/GetAllGroups/", response_model=List[GroupResponse], description="get all groups")
def get_all_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return groups


@router.get("/GetGroupByID/", response_model=GroupResponse, description="get group by id.")
def get_users_by_id(group_id: conint(ge=1), db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()

    if group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group not found")

    return group


@router.get("/GetGroupByName/", response_model=GroupResponse, description="get group by name.")
def get_users_by_name(user_name: str, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.name == user_name).first()

    if group is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group not found")

    return group
