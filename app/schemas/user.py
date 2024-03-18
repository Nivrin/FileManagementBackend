from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    name: str


class UserResponse(BaseModel):
    id: int
    name: str
