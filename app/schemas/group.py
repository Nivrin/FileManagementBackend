from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse


class GroupCreate(BaseModel):
    name: str


class GroupResponse(BaseModel):
    id: int
    name: str
    users: List[UserResponse]
