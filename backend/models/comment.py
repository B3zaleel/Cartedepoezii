#!/usr/bin/python3
from datetime import datetime
from sqlalchemy import Column, ForeignKey, TIMESTAMP, String

from . import Base


class Comment(Base):
    '''Represents a comment on a poem or reply to a comment.'''
    __tablename__ = 'comments'
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
    comment_id = Column(
        String(64),
        nullable=True
    )
    text = Column(
        String(400),
        nullable=False
    )
