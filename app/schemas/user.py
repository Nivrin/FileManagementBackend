from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, examples=["string"])

    class Config:
        extra = "forbid"


class UserResponse(BaseModel):
    name: str
    id: int


class UserShared(BaseModel):
    id: int
