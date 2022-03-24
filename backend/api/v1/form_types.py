#!/usr/bin/python3
'''A module containing JSON body data representations.
'''
from pydantic import BaseModel
from typing import Optional, List


class SignInForm(BaseModel):
    email: str
    password: str


class SignUpForm(BaseModel):
    name: str
    email: str
    password: str


class PasswordResetRequestForm(BaseModel):
    email: str


class PasswordResetForm(BaseModel):
    email: str
    password: str
    resetToken: str


class UserDeleteForm(BaseModel):
    authToken: str
    userId: str


class UserUpdateForm(BaseModel):
    authToken: str
    userId: str
    name: str
    profilePhoto: Optional[str]
    profilePhotoId: str
    removeProfilePhoto: bool
    email: str
    bio: str


class ConnectionForm(BaseModel):
    authToken: str
    userId: str
    followId: str


class PoemAddForm(BaseModel):
    authToken: str
    userId: str
    title: str
    verses: List[str]


class PoemUpdateForm(BaseModel):
    authToken: str
    userId: str
    poemId: str
    title: str
    verses: List[str]


class PoemDeleteForm(BaseModel):
    authToken: str
    userId: str
    poemId: str


class PoemLikeForm(BaseModel):
    authToken: str
    userId: str
    poemId: str


class CommentAddForm(BaseModel):
    authToken: str
    userId: str
    poemId: str
    text: str
    replyTo: Optional[str]


class CommentDeleteForm(BaseModel):
    authToken: str
    userId: str
    commentId: str
