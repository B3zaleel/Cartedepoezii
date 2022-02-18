#!/usr/bin/python3
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    UniqueConstraint
)

from . import Base, BaseModel


class PoemLike(BaseModel, Base):
    '''Represents a like on a poem.'''
    __tablename__ = 'poems_likes'
    __table_args__ = (
        UniqueConstraint(
            'poem_id',
            'user_id',
            name='unique_reaction'
        ),
    )
    poem_id = Column(
        String(64),
        ForeignKey('poems.id'),
        nullable=False
    )
    user_id = Column(
        String(64),
        ForeignKey('users.id'),
        nullable=False
    )
