#!/usr/bin/python3
'''The authentication router's module.
'''
import argon2
import email_validator
import os
import uuid
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import and_

from ..form_types import (
    SignInForm,
    SignUpForm,
    PasswordResetForm,
    PasswordResetRequestForm
)
from ..database import get_session, User
from ..utils.token_handlers import AuthToken, ResetToken
from ..utils.template_renderer import render_template
from ..utils.mailing import deliver_message


router = APIRouter(prefix='/api/v1')


@router.post('/sign-in')
async def sign_in(body: SignInForm):
    '''Signs in a user.'''
    response = {
        'success': False,
        'message': 'Failed to authenticate user.'
    }
    db_session = get_session()
    try:
        email_validator.validate_email(body.email)
        user = db_session.query(User).filter(User.email == body.email).first()
        if user:
            max_sign_in_attempts = int(os.getenv('APP_MAX_SIGNIN_TRIES'))
            try:
                if user.sign_in_attempts >= max_sign_in_attempts:
                    return response
                ph = argon2.PasswordHasher()
                ph.verify(user.password_hash, body.password)
                if user.sign_in_attempts > 1:
                    db_session.query(User).filter(User.email == body.email).update(
                        {
                            User.updated_on: datetime.utcnow(),
                            User.sign_in_attempts: 1,
                        },
                        synchronize_session=False
                    )
                    db_session.commit()
                auth_token = AuthToken(
                    user_id=user.id,
                    email=user.email,
                    secure_text=user.password_hash,
                )
                response = {
                    'success': True,
                    'data': {
                        'userId': user.id,
                        'name': user.name,
                        'authToken': AuthToken.encode(auth_token),
                    }
                }
            except argon2.exceptions.VerificationError:
                # try to lock the user's account
                is_active = user.is_active
                if user.sign_in_attempts + 1 == max_sign_in_attempts:
                    is_active = False
                db_session.query(User).filter(User.email == body.email).update(
                    {
                        User.updated_on: datetime.utcnow(),
                        User.sign_in_attempts: user.sign_in_attempts + 1,
                        User.is_active: is_active,
                    },
                    synchronize_session=False
                )
                db_session.commit()
                if not is_active:
                    deliver_message(
                        body.email,
                        'Your Account Has Been Locked',
                        render_template(
                            'account_locked',
                            name=user.name
                        )
                    )
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.post('/sign-up')
async def sign_up(body: SignUpForm):
    '''Signs up a user.'''
    response = {
        'success': False,
        'message': 'Failed to create account.'
    }
    try:
        # validate body data
        email_validator.validate_email(body.email)
        if len(body.name) > 64:
            response['message'] = 'Name is too long.'
            return response
        db_session = get_session()
        ph = argon2.PasswordHasher()
        try:
            deliver_message(
                body.email,
                'Welcome To Cartedepoezii',
                render_template(
                    'welcome',
                    name=body.name
                )
            )
            pwd_hash = ph.hash(body.password)
            gen_id = str(uuid.uuid4())
            cur_time = datetime.utcnow()
            new_user = User(
                id=gen_id,
                created_on=cur_time,
                updated_on=cur_time,
                name=body.name,
                email=body.email,
                password_hash=pwd_hash,
            )
            db_session.add(new_user)
            db_session.commit()
            auth_token = AuthToken(
                user_id=gen_id,
                email=body.email,
                secure_text=pwd_hash,
            )
            response = {
                'success': True,
                'data': {
                    'userId': gen_id,
                    'name': body.name,
                    'authToken': AuthToken.encode(auth_token)
                }
            }
        except Exception as ex:
            print(ex.args[0])
            db_session.rollback()
            response = {
                'success': False,
                'message': 'Failed to create account.'
            }
        db_session.close()
    except email_validator.EmailNotValidError:
        response['message'] = 'Invalid email.'
    return response


@router.post('/reset-password')
async def request_reset_password(body: PasswordResetRequestForm):
    '''Creates a password reset token for a user.'''
    response = {
        'success': False,
        'message': 'Failed to create password reset token.'
    }
    db_session = get_session()
    try:
        email_validator.validate_email(body.email)
        result = db_session.query(User).filter(
            User.email == body.email
        ).first()
        if result:
            # create reset token
            reset_token = ResetToken(user_id=result.user_id, email=body.email, message='password_reset')
            reset_token_str = ResetToken.encode(reset_token)
            db_session.query(User).filter(and_(
                User.id == result.user_id,
                User.email == body.email
            )).update(
                {
                    User.account_reset_token: reset_token_str
                },
                synchronize_session=False
            )
            db_session.commit()
            response = {
                'success': True,
                'data': {}
            }
            deliver_message(
                body.email,
                'Reset Your Password',
                render_template(
                    'password_reset',
                    name=result.name,
                    token=reset_token_str
                )
            )
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.put('/reset-password')
async def reset_password(body: PasswordResetForm):
    response = {
        'success': False,
        'message': 'Failed to reset password.'
    }
    db_session = get_session()
    try:
        # validate body data and token
        email_validator.validate_email(body.email)
        user = db_session.query(User).filter(
            User.email == body.email
        ).first()
        reset_token = ResetToken.decode(body.resetToken)
        if not reset_token:
            return response
        if reset_token.is_expired():
            response = {
                'success': False,
                'message': 'Password reset token has expired.'
            }
            return response
        valid_conditions = [
            reset_token.email == body.email,
            len(body.password.strip()) > 8,
            reset_token.message == 'password_reset'
        ]
        if all(valid_conditions):
            ph = argon2.PasswordHasher()
            pwd_hash = ph.hash(body.password)
            # reset account
            db_session.query(User).filter(User.email == body.email).update(
                {
                    User.password_hash: pwd_hash,
                    User.account_reset_token: '',
                    User.sign_in_attempts: 1,
                },
                synchronize_session=False
            )
            db_session.commit()
            auth_token = AuthToken(
                user_id=user.id,
                email=body.email,
                secure_text=pwd_hash,
            )
            response = {
                'success': True,
                'data': {
                    'userId': user.id,
                    'name': user.name,
                    'authToken': AuthToken.encode(auth_token)
                }
            }
            deliver_message(
                body.email,
                'Your Password Has Changed',
                render_template(
                    'password_changed',
                    name=user.name
                )
            )
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response
