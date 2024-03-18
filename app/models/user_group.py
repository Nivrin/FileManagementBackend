from sqlalchemy import Column, Integer, ForeignKey, Table

from app.database.database import Base

user_group = Table(
    'user_group',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True)
)

