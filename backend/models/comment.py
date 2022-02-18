#!/usr/bin/python3
from sqlalchemy import Column, ForeignKey, TEXT, String
from sqlalchemy.orm import relationship

from . import Base, BaseModel


class Comment(BaseModel, Base):
    '''Represents a comment on a poem.'''
    __tablename__ = 'comments'
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
        ForeignKey('comments.id'),
        nullable=True
    )
    text = Column(
        String(400),
        nullable=False
    )
