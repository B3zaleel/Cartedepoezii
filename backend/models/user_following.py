#!/usr/bin/python3
from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    TIMESTAMP,
    UniqueConstraint
)

from . import Base, BaseModel


class UserFollowing(Base):
    '''Represents a connection from one user to another.'''
    __tablename__ = 'users_followings'
    __table_args__ = (
        UniqueConstraint(
            'follower_id',
            'following_id',
            name='unique_connection'
        ),
    )
    id = Column(String(64), unique=True, nullable=False, primary_key=True)
    created_on = Column(
        TIMESTAMP(True),
        nullable=False,
        default=datetime.utcnow()
    )
    follower_id = Column(
        String(64),
        ForeignKey('users.id'),
        nullable=False
    )
    following_id = Column(
        String(64),
        ForeignKey('users.id'),
        nullable=False
    )
