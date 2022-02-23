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
    id = Column(
        String(64),
        unique=True,
        nullable=False,
        primary_key=True
    )
    created_on = Column(
        TIMESTAMP(True),
        nullable=False,
        default=datetime.utcnow()
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
