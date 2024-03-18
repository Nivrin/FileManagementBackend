from typing import List, Optional
from pydantic import BaseModel, conint

from app.schemas.user import User
from app.schemas.group import Group


class FileCreate(BaseModel):
    id: Optional[int]
    name: str
    risk: conint(ge=0, le=100)


class FileResponse(BaseModel):
    id: Optional[int]
    name: str
    risk: int
    users: Optional[List[User]] = []
    groups: Optional[List[Group]] = []