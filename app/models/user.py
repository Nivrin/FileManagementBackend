from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.models.user_group import user_group
from app.models.file_user import file_user


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    groups = relationship('Group', secondary=user_group, back_populates='users')
    files = relationship('File', secondary=file_user, back_populates='users')


