#!/usr/bin/python3
from sqlalchemy import (
    Index,
    Column,
    ForeignKey,
    TEXT,
    String
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, cast

from . import Base, BaseModel, create_tsvector


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
    __ts_text_vector__ = create_tsvector(
        cast(func.coalesce(text, ''), postgresql.TEXT)
    )
    __ts_title_vector__ = create_tsvector(
        cast(func.coalesce(title,  ''), postgresql.TEXT)
    )
    __table_args__ = (
        Index(
            'idx_poem_text_tsv',
            __ts_text_vector__,
            postgresql_using='gin'
        ),
        Index(
            'idx_poem_title_tsv',
            __ts_title_vector__,
            postgresql_using='gin'
        ),
    )
