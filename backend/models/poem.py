#!/usr/bin/python3
from sqlalchemy import Column, ForeignKey, TEXT, String
from sqlalchemy.orm import relationship

from . import Base, BaseModel


class Poem(BaseModel, Base):
    '''Represents a poem.'''
    __tablename__ = 'poems'
    user_id = Column(
        String(64),
        ForeignKey('users.id'),
        nullable=False
    )
    title = Column(
        String(256),
        nullable=False,
        default='',
        index=True
    )
    text = Column(
        TEXT,
        nullable=False,
        index=True
    )
    comments = relationship(
        'Comment',
        cascade='all, delete, delete-orphan',
        backref='poem'
    )
    likes = relationship(
        'PoemLike',
        cascade='all, delete, delete-orphan',
        backref='poem'
    )
