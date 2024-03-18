from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import User


class Group(BaseModel):
    id: Optional[int]
    name: str
    users: Optional[List[int]] = []


class GroupResponse(BaseModel):
    name: str
    List: List[User]
