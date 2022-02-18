#!/usr/bin/python3
from fastapi import APIRouter
from fastapi.responses import FileResponse


home_router = APIRouter()


@home_router.get('/')
@home_router.get('/api/v1')
async def root():
    return {
        'code': 200,
        'data': {
            'message': 'Welcome to the Cartedepoezii API.'
        }
    }


@home_router.get('/favicon.ico', response_class=FileResponse)
async def favicon():
    favicon_path = '../static/favicon.ico'
    return favicon_path
