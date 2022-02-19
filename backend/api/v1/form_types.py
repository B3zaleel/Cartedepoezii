#!/usr/bin/python3
from pydantic import BaseModel
from enum import IntEnum
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


class ConnectionForm(BaseModel):
    authToken: str
    userId: str


class PoemAddForm(BaseModel):
    authToken: str
    userId: str
    title: str
    verses: List[str]


class PoemUpdateForm(BaseModel):
    authToken: str
    userId: str
    title: str
    verses: List[str]


class PoemDeleteForm(BaseModel):
    authToken: str
    userId: str
    poemId: str


class CommentAddForm(BaseModel):
    authToken: str
    userId: str
    poemId: str
    text: str
    repliesTo: Optional[str]


class CommentDeleteForm(BaseModel):
    authToken: str
    userId: str
    commentId: str
