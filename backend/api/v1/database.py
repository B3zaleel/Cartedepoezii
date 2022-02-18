#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from models.comment import Comment
from models.poem import Poem
from models.poem_like import PoemLike
from models.user import User
from models.user_following import UserFollowing


def get_engine():
    '''Gets the database engine.
    '''
    SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_DIALECT_DRIVER'),
        os.getenv('DB_USER'),
        os.getenv('DB_PWORD'),
        os.getenv('DB_HOST'),
        os.getenv('DB_PORT'),
        os.getenv('DB_NAME')
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    return engine


def init_db():
    '''Initializes the database.'''
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session():
    '''Creates a new database session.
    '''
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(engine)
    session = SessionLocal()
    return session
