from pydantic import BaseModel,conint, Field
from typing import List, Optional

from app.schemas.group import GroupShared
from app.schemas.user import UserShared


class FileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, examples=["string"])
    risk: conint(ge=0, le=100)

    class Config:
        extra = "forbid"


class FileResponse(BaseModel):
    name: str
    risk: int
    users: List[UserShared]
    groups: List[GroupShared]


class FileTopSharedResponse(BaseModel):
    name: str
    risk: int
    users: List[str]
