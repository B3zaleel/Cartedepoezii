#!/usr/bin/python3
import os
from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse
from imagekitio import ImageKit


home_router = APIRouter()


@home_router.get('/')
@home_router.get('/api')
@home_router.get('/api/v1')
async def root():
    return {
        'success': True,
        'data': {
            'message': 'Welcome to the Cartedepoezii API.'
        }
    }


@home_router.get('/favicon.ico', response_class=FileResponse)
async def favicon():
    favicon_path = '../static/Logo.png'
    return favicon_path


@home_router.get('/api/v1/profile-photo', response_class=RedirectResponse)
async def get_profile_photo(imgId: str):
    imagekit = ImageKit(
        private_key=os.getenv('IMG_CDN_PRI_KEY'),
        public_key=os.getenv('IMG_CDN_PUB_KEY'),
        url_endpoint=os.getenv('IMG_CDN_URL_EPT')
    )
    response = {
        'success': False,
        'message': 'Failed to find URL'
    }
    try:
        img_kit_res = imagekit.get_file_details(imgId)
        img_url = ''
        if img_kit_res['response']:
            img_url = img_kit_res['response']['url']
        if img_kit_res['error']:
            raise ValueError(img_kit_res['error']['message'])
        response = {
            'success': True,
            'data': img_url
        }
    except Exception as ex:
        print(ex.args[0])
    return response
