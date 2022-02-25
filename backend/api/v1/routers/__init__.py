#!/usr/bin/python3
import io
import os
from fastapi import APIRouter
from starlette.responses import FileResponse
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


@home_router.get('/favicon')
@home_router.get('/favicon.ico')
async def favicon():
    favicon_path = 'api/v1/static/Logo.png'
    # favicon_data = []
    # with open(favicon_path, 'rb') as file:
    #     favicon_data = file.read()
    favicon_content = FileResponse(
        path=favicon_path,
        media_type="image/png"
    )
    return favicon_content


@home_router.get('/api/v1/profile-photo')
async def get_profile_photo(imgId: str):
    imagekit = ImageKit(
        private_key=os.getenv('IMG_CDN_PRI_KEY'),
        public_key=os.getenv('IMG_CDN_PUB_KEY'),
        url_endpoint=os.getenv('IMG_CDN_URL_EPT')
    )
    response = {
        'success': False,
        'message': 'Failed to find URL.'
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
