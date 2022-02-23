#!/usr/bin/python3
import argon2
import email_validator
import os
import uuid
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import and_
# import mailer

from ..form_types import (
    SignInForm,
    SignUpForm,
    PasswordResetForm,
    PasswordResetRequestForm
)
from ..database import get_session, User
from ..utils.token_handlers import AuthToken, ResetToken


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
        result = db_session.query(User).filter(User.email == body.email).first()
        if result is not None:
            max_sign_in_attempts = int(os.getenv('APP_MAX_SIGNIN_TRIES'))
            try:
                if result.sign_in_attempts >= max_sign_in_attempts:
                    return response
                ph = argon2.PasswordHasher()
                ph.verify(result.password_hash, body.password)
                if result.sign_in_attempts > 1:
                    db_session.query(User).filter(User.email == body.email).update(
                        {
                            User.updated_on: datetime.utcnow(),
                            User.sign_in_attempts: 1,
                        },
                        synchronize_session=False
                    )
                    db_session.commit()
                auth_token = AuthToken(
                    user_id=result.id,
                    email=result.email,
                    secure_text=result.password_hash,
                )
                response = {
                    'success': True,
                    'data': {
                        'userId': result.id,
                        'authToken': AuthToken.encode(auth_token),
                    }
                }
            except argon2.exceptions.VerificationError:
                is_active = False if result.sign_in_attempts + 1 == max_sign_in_attempts else True
                db_session.query(User).filter(User.email == body.email).update(
                    {
                        User.updated_on: datetime.utcnow(),
                        User.sign_in_attempts: result.sign_in_attempts + 1,
                        User.is_active: is_active,
                    },
                    synchronize_session=False
                )
                db_session.commit()
                if not is_active:
                    pass
                    # TODO: send an account locked message to the user \
                    # with an option to reset password.
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.post('/sign-up')
async def sign_up(body: SignUpForm):
    '''Signs up a user.'''
    response = None
    try:
        email_validator.validate_email(body.email)
        db_session = get_session()
        ph = argon2.PasswordHasher()
        try:
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
    except (email_validator.EmailNotValidError,
            email_validator.EmailSyntaxError,
            email_validator.EmailUndeliverableError):
        response = {
            'success': False,
            'message': 'Invalid email.'
        }
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
        result = db_session.query(User).filter(and_(
            User.id == body.userId,
            User.email == body.email
        )).first()
        if result:
            reset_token = ResetToken(user_id=body.userId, email=body.email, message='password_reset')
            db_session.query(User).filter(and_(
                User.id == body.userId,
                User.email == body.email
            )).update(
                {
                    User.account_reset_token: ResetToken.encode(reset_token)
                },
                synchronize_session=False
            )
            db_session.commit()
            response = {
                'success': True,
                'data': {}
            }
            # TODO: Send a password reset request to the user's email
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
        email_validator.validate_email(body.email)
        user = db_session.query(User).filter(and_(
            User.id == body.userId,
            User.email == body.email
        )).first()
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
            reset_token.user_id == body.userId,
            reset_token.email == body.email,
            len(body.password.strip()) > 8,
            reset_token.message == 'password_reset'
        ]
        if all(valid_conditions):
            ph = argon2.PasswordHasher()
            pwd_hash = ph.hash(body.password)
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
                    'authToken': AuthToken.encode(auth_token),
                    'userId': user.id
                }
            }
            # TODO: Send a password changed confirmation message
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response
