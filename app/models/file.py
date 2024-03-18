from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.file_group import file_group
from app.models.file_user import file_user

from app.database.database import Base


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    risk = Column(Integer)

    users = relationship('User', secondary=file_user, back_populates='files')
    groups = relationship('Group', secondary=file_group, back_populates='files')
