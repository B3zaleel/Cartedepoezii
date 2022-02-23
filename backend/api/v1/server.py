#!/usr/bin/python3
import os
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from .router import inject_routers
from .middleware import inject_middlewares


app = FastAPI()
inject_middlewares(app)
inject_routers(app)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    default_message = 'Request failed.'
    res = {
        'success': False,
        'message': str(exc) if exc else default_message
    }
    return JSONResponse(res)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    default_message = 'Request failed.'
    res = {
        'success': False,
        'message': str(exc) if exc else default_message
    }
    return JSONResponse(res)


if __name__ == '__main__':
    uvicorn.run(
        'api.v1.server:app',
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', '5000')),
        log_level='info',
    )
