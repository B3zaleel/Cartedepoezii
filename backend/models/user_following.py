#!/usr/bin/python3
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    UniqueConstraint
)

from . import Base, BaseModel


class UserFollowing(BaseModel, Base):
    '''Represents a reaction on a poem.'''
    __tablename__ = 'users_followings'
    __table_args__ = (
        UniqueConstraint(
            'follower_id',
            'following_id',
            name='unique_connection'
        ),
    )
    follower_id = Column(
        String(64),
        ForeignKey('poems.id'),
        nullable=False
    )
    following_id = Column(
        String(64),
        ForeignKey('users.id'),
        nullable=False
    )
