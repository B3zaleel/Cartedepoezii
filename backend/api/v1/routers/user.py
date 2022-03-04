#!/usr/bin/python3
import os
import base64
import email_validator
from datetime import datetime
from fastapi import APIRouter
from imagekitio import ImageKit
from sqlalchemy import and_

from ..form_types import UserDeleteForm, UserUpdateForm
from ..database import (
    get_session,
    User,
    UserFollowing,
    Poem,
    PoemLike,
    Comment,
)
from ..utils.token_handlers import AuthToken


router = APIRouter(prefix='/api/v1')


@router.get('/user')
async def get_user(id: str, token=''):
    response = {
        'success': False,
        'message': 'Failed to find user.'
    }
    auth_token = AuthToken.decode(token)
    if id is None:
        return response
    user_id = auth_token.user_id if auth_token is not None else ''
    db_session = get_session()
    try:
        user = db_session.query(User).filter(User.id == id).first()
        if user:
            followers = db_session.query(UserFollowing).filter(
                UserFollowing.following_id == user.id
            ).all()
            followings = db_session.query(UserFollowing).filter(
                UserFollowing.follower_id == user.id
            ).all()
            poems = db_session.query(Poem).filter(
                Poem.user_id == user.id
            ).all()
            likes = db_session.query(PoemLike).filter(
                PoemLike.user_id == user.id
            ).all()
            comments = db_session.query(Comment).filter(
                Comment.user_id == user.id
            ).all()
            cur_usr_ctn = db_session.query(UserFollowing).filter(and_(
                UserFollowing.follower_id == user_id,
                UserFollowing.following_id == user.id,
            )).first()
            followers_count = len(followers) if followers else 0
            followings_count = len(followings) if followings else 0
            poems_count = len(poems) if poems else 0
            likes_count = len(likes) if likes else 0
            comments_count = len(comments) if comments else 0
            response = {
                'success': True,
                'data': {
                    'id': user.id,
                    'joined': user.created_on.isoformat(),
                    'name': user.name,
                    'email': user.email if user.id == user_id else '',
                    'bio': user.bio,
                    'profilePhotoId': user.profile_photo_id,
                    'followersCount': followers_count,
                    'followingsCount': followings_count,
                    'poemsCount': poems_count,
                    'likesCount': likes_count,
                    'commentsCount': comments_count,
                    'isFollowing': cur_usr_ctn is not None,
                }
            }
    finally:
        db_session.close()
    return response


@router.put('/user')
async def update_user_info(body: UserUpdateForm):
    response = {
        'success': False,
        'message': 'Failed to update user info.'
    }
    auth_token = AuthToken.decode(body.authToken)
    wrong_conditions = [
        auth_token is None,
        auth_token is not None and (auth_token.user_id != body.userId)
    ]
    if any(wrong_conditions):
        return response
    db_session = get_session()
    imagekit = ImageKit(
        private_key=os.getenv('IMG_CDN_PRI_KEY'),
        public_key=os.getenv('IMG_CDN_PUB_KEY'),
        url_endpoint=os.getenv('IMG_CDN_URL_EPT')
    )
    try:
        email_validator.validate_email(body.email)
        profile_picture_file_id = body.profilePhotoId.strip()
        if body.removeProfilePhoto:
            if profile_picture_file_id:
                imagekit.delete_file(profile_picture_file_id)
                profile_picture_file_id = ''
        if body.profilePhoto and not body.removeProfilePhoto:
            if body.profilePhotoId.strip():
                imagekit.delete_file(body.profilePhotoId)
            user = db_session.query(User).filter(User.id == body.userId).first()
            if user.profile_photo_id:
                imagekit.delete_file(user.profile_photo_id)
            # with open('foo.jpeg', 'wb') as file:
            #     file.write(file_bytes)
            img_kit_res = imagekit.upload_file(
                file=body.profilePhoto,
                file_name='{}'.format(
                    body.userId.replace('-', ''),
                    # profilePhoto.content_type.split('/')[1]
                ),
                options={
                    'folder': 'cartedepoezii/profile_photos/',
                    'is_private_file': False
                }
            )
            if img_kit_res['response']:
                profile_picture_file_id = img_kit_res['response']['fileId']
                print(profile_picture_file_id)
            if img_kit_res['error']:
                raise ValueError(img_kit_res['error']['message'])
        db_session.query(User).filter(User.id == body.userId).update(
            {
                User.updated_on: datetime.utcnow(),
                User.name: body.name,
                User.profile_photo_id: profile_picture_file_id,
                User.email: body.email,
                User.bio: body.bio
            },
            synchronize_session=False
        )
        db_session.commit()
        new_auth_token = AuthToken(
            user_id=body.userId,
            email=body.email,
            secure_text=auth_token.secure_text
        )
        response = {
            'success': True,
            'data': {
                'authToken': AuthToken.encode(new_auth_token),
                'profilePhotoId': profile_picture_file_id
            }
        }
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.delete('/user')
async def remove_user(body: UserDeleteForm):
    response = {
        'success': False,
        'message': 'Failed to remove user.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        return response
    db_session = get_session()
    try:
        db_session.query(UserFollowing).filter(and_(
            UserFollowing.follower_id == auth_token.user_id,
            UserFollowing.following_id == body.followId,
        )).delete(
            synchronize_session=False
        )
        db_session.commit()
        response = {
            'success': True,
            'data': {}
        }
    finally:
        db_session.close()
    return response
