#!/usr/bin/python3
import os
import uvicorn
from fastapi import FastAPI

from .router import inject_routers
from .middleware import inject_middlewares


app = FastAPI()
inject_middlewares(app)
inject_routers(app)


if __name__ == '__main__':
    uvicorn.run(
        'server:app',
        host=os.getenv('HOST', '0.0.0.0'),
        port=os.getenv('PORT', '5000'),
        log_level='info',
    )
