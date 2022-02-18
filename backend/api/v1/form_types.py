#!/usr/bin/python3
from pydantic import BaseModel
from enum import IntEnum
from typing import Optional, List


class SignInForm(BaseModel):
    email: str
    password: str


class SignUpForm(BaseModel):
    email: str
    password: str
    name: str
    agreesToTOS: bool
    admin_pass: Optional[str]


class PasswordResetRequestForm(BaseModel):
    email: str


class PasswordResetForm(BaseModel):
    email: str
    resetToken: str
    password: str
    confirmPassword: str
