from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.user_group import user_group
from app.models.file_group import file_group


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    users = relationship('User', secondary=user_group, back_populates='groups')
    files = relationship('File', secondary=file_group, back_populates='groups')
