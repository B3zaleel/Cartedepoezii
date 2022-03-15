#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware


def inject_middlewares(app: FastAPI):
    '''Adds all required middlewares to the given application.
    '''
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['https://cartedepoezii.netlify.app'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.add_middleware(GZipMiddleware, minimum_size=1024)
