#!/usr/bin/python3
from sqlalchemy import (
    Boolean,
    Index,
    Column,
    TEXT,
    Integer,
    String
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, cast

from . import Base, BaseModel, create_tsvector


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
    account_reset_token = Column(
        TEXT,
        nullable=True,
        default=''
    )
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
    __ts_name_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )
    __ts_bio_vector__ = create_tsvector(
        cast(func.coalesce(bio, ''), postgresql.TEXT)
    )
    __table_args__ = (
        Index(
            'idx_user_name_tsv',
            __ts_name_vector__,
            postgresql_using='gin'
        ),
        Index(
            'idx_user_bio_tsv',
            __ts_bio_vector__,
            postgresql_using='gin'
        ),
    )
