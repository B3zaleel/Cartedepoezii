#!/usr/bin/python3
from fastapi import FastAPI

from .routers import (
    home_router,
    auth,
    media,
    poem,
    user
)


def inject_routers(app: FastAPI):
    '''Adds all required routers to the given application.
    '''
    app.include_router(home_router)
    app.include_router(auth.router)
    app.include_router(media.router)
    app.include_router(poem.router)
    app.include_router(user.router)
