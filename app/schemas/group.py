from pydantic import BaseModel
from typing import List

from app.schemas.user import UserResponse


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    name: str
    users: List[UserResponse]


class GroupShared(BaseModel):
    id: int
