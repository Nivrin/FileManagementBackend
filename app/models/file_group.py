from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database.database import Base

file_group = Table(
    'file_group',
    Base.metadata,
    Column('file_id', Integer, ForeignKey('file.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)
