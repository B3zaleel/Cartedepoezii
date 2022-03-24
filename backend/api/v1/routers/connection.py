#!/usr/bin/python3
'''The connection router's module.
'''
import re
import uuid
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import and_

from ..form_types import ConnectionForm
from ..database import get_session, User, UserFollowing
from ..utils.token_handlers import AuthToken
from ..utils.pagination import extract_page


router = APIRouter(prefix='/api/v1')


@router.get('/followers')
async def get_users_followers(
    id='',
    token='',
    span='12',
    after='',
    before=''
    ):
    '''Retrieves a user's followers.
    '''
    response = {
        'success': False,
        'message': 'Failed to find followers.'
    }
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token else None
    db_session = get_session()
    try:
        # sanitize the span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        user_followers = db_session.query(UserFollowing).filter(
            UserFollowing.following_id == id
        ).all()
        user_followers_objs = []
        if user_followers:
            for user_follower in user_followers:
                user = db_session.query(User).filter(
                    User.id == user_follower.follower_id
                ).first()
                if not user:
                    continue
                # get current user's connection with this user
                cur_usr_ctn = db_session.query(UserFollowing).filter(and_(
                    UserFollowing.follower_id == user_id,
                    UserFollowing.following_id == user.id,
                )).first()
                obj = {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id,
                    'isFollowing': cur_usr_ctn is not None,
                }
                user_followers_objs.append(obj)
        response = {
            'success': True,
            'data': extract_page(
                user_followers_objs,
                span,
                after,
                before,
                True,
                lambda x: x['id']
            )
        }
    finally:
        db_session.close()
    return response


@router.get('/followings')
async def get_users_followings(
    id='',
    token='',
    span='12',
    after='',
    before=''
    ):
    '''Retrieves users followed by a given user.
    '''
    response = {
        'success': False,
        'message': 'Failed to find followings.'
    }
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token else None
    db_session = get_session()
    try:
        # sanitize the span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        users_followings = db_session.query(UserFollowing).filter(
            UserFollowing.follower_id == id
        ).all()
        users_followings_objs = []
        if users_followings:
            for user_following in users_followings:
                user = db_session.query(User).filter(
                    User.id == user_following.following_id
                ).first()
                if not user:
                    continue
                cur_usr_ctn = db_session.query(UserFollowing).filter(and_(
                    UserFollowing.follower_id == user_id,
                    UserFollowing.following_id == user.id,
                )).first()
                obj = {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id,
                    'isFollowing': cur_usr_ctn is not None,
                }
                users_followings_objs.append(obj)
        response = {
            'success': True,
            'data': extract_page(
                users_followings_objs,
                span,
                after,
                before,
                False,
                lambda x: x['id']
            )
        }
    finally:
        db_session.close()
    return response


@router.put('/follow')
async def change_connection(body: ConnectionForm):
    '''Toggles the connection between two users.
    '''
    response = {
        'success': False,
        'message': 'Failed to follow user.'
    }
    # validate body data
    auth_token = AuthToken.decode(body.authToken)
    wrong_conditions = [
        auth_token is None,
        auth_token is not None and (auth_token.user_id != body.userId),
        body.userId == body.followId
    ]
    if any(wrong_conditions):
        return response
    db_session = get_session()
    try:
        cur_usr_ctn = db_session.query(UserFollowing).filter(and_(
            UserFollowing.follower_id == auth_token.user_id,
            UserFollowing.following_id == body.followId,
        )).first()
        if cur_usr_ctn:
            # remove connection
            db_session.query(UserFollowing).filter(and_(
                UserFollowing.follower_id == auth_token.user_id,
                UserFollowing.following_id == body.followId,
            )).delete(
                synchronize_session=False
            )
            db_session.commit()
            response = {
                'success': True,
                'data': {'status': False}
            }
        else:
            # create connection
            new_connection = UserFollowing(
                id=str(uuid.uuid4()),
                created_on=datetime.utcnow(),
                follower_id=body.userId,
                following_id=body.followId
            )
            db_session.add(new_connection)
            db_session.commit()
            response = {
                'success': True,
                'data': {'status': True}
            }
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response
