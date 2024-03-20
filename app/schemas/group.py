from pydantic import BaseModel
from typing import List

from app.schemas.user import UserResponse


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str
    users: List[UserResponse]
