#!/usr/bin/python3
'''The API server module.
'''
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


async def exception_handler(request, exc):
    '''Converts exceptions to a JSON response.
    '''
    default_message = '[{}]: Request failed.'.format(exc.__class__.__name__)
    res = {
        'success': False,
        'message': str(exc) if exc else default_message
    }
    return JSONResponse(res)


app.add_exception_handler(StarletteHTTPException, exception_handler)
app.add_exception_handler(RequestValidationError, exception_handler)
app.add_exception_handler(Exception, exception_handler)


if __name__ == '__main__':
    uvicorn.run(
        'api.v1.server:app',
        host=os.getenv('HOST', '0.0.0.0'),
        port=5000,
        log_level='info',
    )
