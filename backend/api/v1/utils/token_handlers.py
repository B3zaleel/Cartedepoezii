#!/usr/bin/python3
'''A module for decoding and encoding tokens.
'''
import os
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from json import JSONDecoder, JSONEncoder

from ..database import get_session, User


class AuthToken:
    '''Represents an object for managing user authentication tokens.'''
    def __init__(self, user_id='', email='', secure_text='', expires=None):
        self.user_id = user_id
        self.email = email
        self.secure_text = secure_text
        if expires:
            self.expires = expires

    @property
    def user_id(self):
        return self.__userId

    @user_id.setter
    def user_id(self, value):
        if type(value) is str:
            self.__userId = value
        else:
            raise TypeError('Invalid type.')

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if type(value) is str:
            self.__email = value
        else:
            raise TypeError('Invalid type.')

    @property
    def secure_text(self):
        return self.__secureText

    @secure_text.setter
    def secure_text(self, value):
        if type(value) is str:
            self.__secureText = value
        else:
            raise TypeError('Invalid type.')

    @property
    def expires(self):
        return self.__expiryDate

    @expires.setter
    def expires(self, value):
        if type(value) is str:
            self.__expiryDate = datetime.fromisoformat(value)
        else:
            raise TypeError('Invalid type.')

    def is_expired(self):
        '''Checks if this token is expired.
        '''
        if not self.expires:
            return False
        cur_time = datetime.utcnow()
        not_expired_conditions = [
            cur_time.year <= self.expires.year,
            cur_time.month <= self.expires.month,
            cur_time.day <= self.expires.day,
            cur_time.hour <= self.expires.hour,
            cur_time.minute <= self.expires.minute,
            cur_time.second <= self.expires.second
        ]
        return all(not_expired_conditions)

    @staticmethod
    def decode(token: str):
        '''Decodes an authentication string into an AuthToken object.'''
        key = bytes(os.getenv('APP_SECRET_KEY'), 'utf-8')
        f = Fernet(key)
        db_session = get_session()
        try:
            auth_token_dict = JSONDecoder().decode(
                f.decrypt(bytes(token, 'utf-8')).decode('utf-8')
            )
            valid_keys = {
                'userId': str,
                'email': str,
                'secureText': str,
                'expires': str
            }
            if type(auth_token_dict) is not dict:
                raise TypeError('Invalid token.')
            for key, val in auth_token_dict.items():
                if key in valid_keys:
                    if type(val) is not valid_keys[key]:
                        raise TypeError('Invalid token.')
                else:
                    raise KeyError('Invalid token.')
            cur_datetime = datetime.utcnow()
            exp_datetime = datetime.fromisoformat(auth_token_dict['expires'])
            if exp_datetime >= cur_datetime:
                raise ValueError('Token expired.')
            user = db_session.query(User).filter(
                User.id == auth_token_dict['userId']
            ).first()
            valid_conds = (
                user is not None,
                user and user.is_active,
                user and user.email == auth_token_dict['email'],
                user and user.password_hash == auth_token_dict['secureText'],
            )
            if not all(valid_conds):
                raise ValueError('Invalid token.')
            db_session.close()
            auth_token = AuthToken(
                user_id=auth_token_dict['userId'],
                email=auth_token_dict['email'],
                secure_text=auth_token_dict['secureText'],
                expires = auth_token_dict['expires']
            )
            return auth_token
        except Exception as ex:
            print(ex)
            db_session.close()
            return None

    @staticmethod
    def encode(auth_token) -> str:
        '''Encodes an AuthToken object to an authentication string.'''
        key = bytes(os.getenv('APP_SECRET_KEY'), 'utf-8')
        f = Fernet(key)
        try:
            cur_datetime = datetime.utcnow()
            time_span = timedelta(days=30)
            exp_datetime = cur_datetime - time_span
            auth_token_txt = JSONEncoder().encode(
                {
                    'userId': auth_token.user_id,
                    'email': auth_token.email,
                    'secureText': auth_token.secure_text,
                    'expires': exp_datetime.isoformat(),
                }
            )
            return f.encrypt(bytes(auth_token_txt, 'utf-8')).decode('utf-8')
        except Exception:
            return ''


class ResetToken:
    '''Represents an object for managing user account reset tokens.'''
    def __init__(self, user_id='', email='', message='', expires=None):
        self.user_id = user_id
        self.email = email
        self.message = message
        if expires:
            self.expires = expires

    @property
    def user_id(self):
        return self.__userId

    @user_id.setter
    def user_id(self, value):
        if type(value) is str:
            self.__userId = value
        else:
            raise TypeError('Invalid type.')

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if type(value) is str:
            self.__email = value
        else:
            raise TypeError('Invalid type.')

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if type(value) is str:
            self.__message = value
        else:
            raise TypeError('Invalid type.')

    @property
    def expires(self):
        return self.__expiryDate

    @expires.setter
    def expires(self, value):
        if type(value) is str:
            self.__expiryDate = datetime.fromisoformat(value)
        else:
            raise TypeError('Invalid type.')

    def is_expired(self):
        '''Checks if this token is expired.
        '''
        if not self.expires:
            return False
        cur_time = datetime.utcnow()
        not_expired_conditions = [
            cur_time.year <= self.expires.year,
            cur_time.month <= self.expires.month,
            cur_time.day <= self.expires.day,
            cur_time.hour <= self.expires.hour,
            cur_time.minute <= self.expires.minute,
            cur_time.second <= self.expires.second
        ]
        return all(not_expired_conditions)

    @staticmethod
    def decode(token: str):
        '''Decodes a reset token string into a ResetToken object.'''
        key = bytes(os.getenv('APP_SECRET_KEY'), 'utf-8')
        f = Fernet(key)
        db_session = get_session()
        try:
            reset_token_dict = JSONDecoder().decode(
                f.decrypt(bytes(token, 'utf-8')
            ).decode('utf-8'))
            valid_keys = {
                'userId': str,
                'email': str,
                'message': str,
                'expires': str
            }
            if type(reset_token_dict) is not dict:
                raise TypeError('Invalid token.')
            for key, val in reset_token_dict.items():
                if key in valid_keys:
                    if type(val) is not valid_keys[key]:
                        raise TypeError('Invalid token.')
                else:
                    raise KeyError('Invalid token.')
            cur_datetime = datetime.utcnow()
            exp_datetime = datetime.fromisoformat(reset_token_dict['expires'])
            if exp_datetime >= cur_datetime:
                raise ValueError('Token expired.')
            user = db_session.query(User).filter(
                User.id == reset_token_dict['id']
            ).first()
            valid_conds = (
                user is not None,
                user and user.is_active,
                user and user.email == reset_token_dict['email']
            )
            if not all(valid_conds):
                raise ValueError('Invalid token.')
            db_session.close()
            reset_token = ResetToken(
                user_id=reset_token_dict['userId'],
                email=reset_token_dict['email'],
                message=reset_token_dict['message'],
            )
            reset_token.expires = reset_token_dict['expires'],
            return reset_token
        except Exception:
            db_session.close()
            return None

    @staticmethod
    def encode(reset_token) -> str:
        '''Encodes a ResetToken object to a reset token string.'''
        key = bytes(os.getenv('APP_SECRET_KEY'), 'utf-8')
        f = Fernet(key)
        try:
            cur_datetime = datetime.utcnow()
            time_span = timedelta(days=30)
            exp_datetime = cur_datetime - time_span
            reset_token_txt = JSONEncoder().encode(
                {
                    'id': reset_token.user_id,
                    'email': reset_token.email,
                    'message': reset_token.message,
                    'expires': exp_datetime.isoformat(),
                }
            )
            return f.encrypt(bytes(reset_token_txt, 'utf-8')).decode('utf-8')
        except Exception:
            return ''
