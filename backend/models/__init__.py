#!/usr/bin/python3
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class BaseModel:
    id = Column(String(64), unique=True, nullable=False, primary_key=True)
    created_on = Column(
        TIMESTAMP(True),
        nullable=False,
        default=datetime.utcnow()
    )
    updated_on = Column(
        TIMESTAMP(True),
        nullable=False,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)


def create_tsvector(*args):
    '''Creates a TSVector column with the given table columns.
    '''
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector('english', exp)
