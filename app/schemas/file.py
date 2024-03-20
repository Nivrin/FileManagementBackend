from pydantic import BaseModel,conint, Field
from typing import List, Optional

from app.schemas.group import GroupResponse
from app.schemas.user import UserResponse


class FileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, examples=["string"])
    risk: conint(ge=0, le=100)

    class Config:
        extra = "forbid"


class FileResponse(BaseModel):
    id: int
    name: str
    risk: int
    users: Optional[List[UserResponse]] = []
    groups: Optional[List[GroupResponse]] = []


class FileTopSharedResponse(BaseModel):
    name: str
    risk: int
    users: List[str]
