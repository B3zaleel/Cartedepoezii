#!/usr/bin/python3
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
    span=12,
    after='',
    before=''
    ):
    response = {
        'success': False,
        'message': 'Failed to find followers.'
    }
    if span < 0:
        span = -span
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        result = db_session.query(
            UserFollowing).filter(UserFollowing.following_id == id).all()
        if result is not None:
            new_result = []
            for item in result:
                user = db_session.query(
                    User).filter(User.id == item.follower_id).first()
                if not user:
                    continue
                cur_usr_ctn = db_session.query(
                    UserFollowing).filter(
                        and_(
                            UserFollowing.follower_id == user_id,
                            UserFollowing.following_id == user.id,
                    )).first()
                obj = {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id,
                    'isFollowing': cur_usr_ctn is not None,
                }
                new_result.append(obj)
            response = {
                'success': True,
                'data': extract_page(
                    new_result,
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


@router.get('/followings')
async def get_users_followings(
    id='',
    token='',
    span=12,
    after='',
    before=''
    ):
    response = {
        'success': False,
        'message': 'Failed to find followings.'
    }
    if span < 0:
        span = -span
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        result = db_session.query(
            UserFollowing).filter(UserFollowing.follower_id == id).all()
        if result is not None:
            new_result = []
            for item in result:
                user = db_session.query(
                    User).filter(User.id == item.following_id).first()
                if not user:
                    continue
                cur_usr_ctn = db_session.query(
                    UserFollowing).filter(
                        and_(
                            UserFollowing.follower_id == user_id,
                            UserFollowing.following_id == user.id,
                    )).first()
                obj = {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id,
                    'isFollowing': cur_usr_ctn is not None,
                }
                new_result.append(obj)
            response = {
                'success': True,
                'data': extract_page(
                    new_result,
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
    response = {
        'success': False,
        'message': 'Failed to follow user.'
    }
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
        cur_usr_ctn = db_session.query(
            UserFollowing).filter(
                and_(
                    UserFollowing.follower_id == auth_token.user_id,
                    UserFollowing.following_id == body.followId,
            )).first()
        if cur_usr_ctn:
            # remove
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
            new_connection = UserFollowing(
                id=str(uuid.uuid4()),
                created_on=datetime.utcnow(),
                follower_id=body.userId,
                following_id=body.followId,
                name=body.name
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
