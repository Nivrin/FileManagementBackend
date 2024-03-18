from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database.database import Base

file_user = Table(
    'file_user',
    Base.metadata,
    Column('file_id', Integer, ForeignKey('file.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True)
)
