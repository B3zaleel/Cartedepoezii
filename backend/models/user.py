#!/usr/bin/python3
from sqlalchemy import Boolean, Column, TEXT, Integer, String
from sqlalchemy.orm import relationship

from . import Base, BaseModel


class User(BaseModel, Base):
    '''Represents a user.'''
    __tablename__ = 'users'
    email = Column(
        String(320),
        nullable=False,
        unique=True,
        index=True
    )
    name = Column(String(60))
    bio = Column(String(256), default='')
    profile_photo_id = Column(
        TEXT,
        nullable=False,
        default=''
    )
    password_hash = Column(
        TEXT,
        nullable=False
    )
    sign_in_attempts = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    poems = relationship(
        'Poem',
        cascade='all, delete, delete-orphan',
        backref='user'
    )
    comments = relationship(
        'Comment',
        cascade='all, delete, delete-orphan',
        backref='user'
    )
