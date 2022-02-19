#!/usr/bin/python3
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, TIMESTAMP, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_DIALECT_DRIVER'),
    os.getenv('DB_USER'),
    os.getenv('DB_PWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME')
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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
        default=datetime.utcnow()
    )

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
