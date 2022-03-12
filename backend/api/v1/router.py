#!/usr/bin/python3
from fastapi import FastAPI

from .routers import (
    authentication,
    home_router,
    comment,
    connection,
    poem,
    search,
    user
)


def inject_routers(app: FastAPI):
    '''Adds all required routers to the given application.
    '''
    app.include_router(home_router)
    app.include_router(authentication.router)
    app.include_router(comment.router)
    app.include_router(connection.router)
    app.include_router(poem.router)
    app.include_router(search.router)
    app.include_router(user.router)
