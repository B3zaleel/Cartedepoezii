#!/usr/bin/python3
'''The poem router's module.
'''
import json
import re
import uuid
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import and_

from ..form_types import (
    PoemAddForm,
    PoemUpdateForm,
    PoemLikeForm,
    PoemDeleteForm
)
from ..database import (
    get_session,
    User,
    Comment,
    Poem,
    PoemLike,
    UserFollowing
)
from ..utils.token_handlers import AuthToken
from ..utils.pagination import extract_page


router = APIRouter(prefix='/api/v1')


@router.get('/poem')
async def get_poem(id: str, token: str):
    '''Retrieves information about a given poem.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poem.'
    }
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        poem = db_session.query(Poem).filter(
            Poem.id == id
        ).first()
        if poem:
            # get the relevant information related to the poem
            user = db_session.query(User).filter(
                User.id == poem.user_id
            ).first()
            if not user:
                return response
            comments = db_session.query(Comment).filter(and_(
                Comment.poem_id == id,
                Comment.comment_id == None
            )).all()
            comments_count = len(comments) if comments else 0
            likes = db_session.query(PoemLike).filter(
                PoemLike.poem_id == id
            ).all()
            likes_count = len(likes) if likes else 0
            is_liked_by_user = False
            if user_id:
                # check current users reaction on this poem
                poem_interaction = db_session.query(PoemLike).filter(and_(
                    PoemLike.poem_id == id,
                    PoemLike.user_id == user_id
                )).first()
                if poem_interaction:
                    is_liked_by_user = True
            response = {
                'success': True,
                'data': {
                    'id': poem.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'title': poem.title,
                    'publishedOn': poem.created_on.isoformat(),
                    'verses': json.JSONDecoder().decode(poem.text),
                    'commentsCount': comments_count,
                    'likesCount': likes_count,
                    'isLiked': is_liked_by_user
                }
            }
    finally:
        db_session.close()
    return response


@router.post('/poem')
async def add_poem(body: PoemAddForm):
    '''Creates a new poem.
    '''
    response = {
        'success': False,
        'message': 'Failed to add poem.'
    }
    # validate body data
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    if len(body.title) > 256:
        response['message'] = 'Title is too long.'
        return response
    if len(body.verses) < 1:
        response['message'] = 'Verses is too short.'
        return response
    if not all(list(map(lambda x: len(x.strip()) > 1, body.verses))):
        response['message'] = 'Verses is too short.'
        return response
    db_session = get_session()
    try:
        gen_id = str(uuid.uuid4())
        cur_time = datetime.utcnow()
        verses_txt = json.JSONEncoder().encode(body.verses)
        poem = Poem(
            id=gen_id,
            created_on=cur_time,
            updated_on=cur_time,
            user_id=body.userId,
            title=body.title,
            text=verses_txt
        )
        db_session.add(poem)
        db_session.commit()
        response = {
            'success': True,
            'data': {
                'id': gen_id,
                'createdOn': cur_time.isoformat(),
                'repliesCount': 0,
                'likesCount': 0
            }
        }
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.put('/poem')
async def update_poem(body: PoemUpdateForm):
    '''Edits an existing poem.
    '''
    response = {
        'success': False,
        'message': 'Failed to update poem.'
    }
    # validate body data
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    if len(body.title) > 256:
        response['message'] = 'Title is too long.'
        return response
    if len(body.verses) < 1:
        response['message'] = 'Verses is too short.'
        return response
    if not all(list(map(lambda x: len(x.strip()) > 1, body.verses))):
        response['message'] = 'Verses is too short.'
        return response
    db_session = get_session()
    try:
        cur_time = datetime.utcnow()
        verses_txt = json.JSONEncoder().encode(body.verses)
        db_session.query(Poem).filter(Poem.id == body.poemId).update(
            {
                Poem.title: body.title,
                Poem.updated_on: cur_time,
                Poem.text: verses_txt
            },
            synchronize_session=False
        )
        db_session.commit()
        response = {
            'success': True,
            'data': {}
        }
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.delete('/poem')
async def remove_poem(body: PoemDeleteForm):
    '''Deletes a poem.
    '''
    response = {
        'success': False,
        'message': 'Failed to remove poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    db_session = get_session()
    try:
        poem = db_session.query(Poem).filter(and_(
            Poem.id == body.poemId,
            Poem.user_id == body.userId,
        )).first()
        if poem:
            db_session.query(PoemLike).filter(
                PoemLike.poem_id == body.poemId,
            ).delete(
                synchronize_session=False
            )
            db_session.query(Comment).filter(
                Comment.poem_id == body.poemId,
            ).delete(
                synchronize_session=False
            )
            db_session.query(Poem).filter(and_(
                Poem.id == body.poemId,
                Poem.user_id == body.userId,
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


@router.put('/like-poem')
async def like_poem(body: PoemLikeForm):
    '''Toggles a user's reaction on a poem.
    '''
    response = {
        'success': False,
        'message': 'Failed to like poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    db_session = get_session()
    try:
        cur_usr_fav = db_session.query(PoemLike).filter(and_(
            PoemLike.user_id == auth_token.user_id,
            PoemLike.poem_id == body.poemId,
        )).first()
        if cur_usr_fav:
            # dislike poem
            db_session.query(PoemLike).filter(and_(
                PoemLike.user_id == auth_token.user_id,
                PoemLike.poem_id == body.poemId,
            )).delete(
                synchronize_session=False
            )
            db_session.commit()
            response = {
                'success': True,
                'data': {'status': False}
            }
        else:
            # like poem
            new_favourite = PoemLike(
                id=str(uuid.uuid4()),
                created_on=datetime.utcnow(),
                user_id=body.userId,
                poem_id=body.poemId,
            )
            db_session.add(new_favourite)
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


@router.get('/poems-user-created')
async def get_created_poems(userId, token='', span='', after='', before=''):
    '''Retrieves poems created by the current user.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poems created by the user.'
    }
    if not userId:
        return response
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        # sanitize span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        poems_created = db_session.query(Poem).filter(
            Poem.user_id == userId
        ).all()
        user_poems = []
        if poems_created:
            user = db_session.query(User).filter(
                User.id == userId
            ).first()
            if not user:
                return response
            for poem in poems_created:
                # retrieve information related to the current poem
                comments = db_session.query(Comment).filter(and_(
                    Comment.poem_id == poem.id,
                    Comment.comment_id == None
                )).all()
                comments_count = len(comments) if comments else 0
                likes = db_session.query(PoemLike).filter(
                    PoemLike.poem_id == poem.id
                ).all()
                likes_count = len(likes) if likes else 0
                is_liked_by_user = False
                if user_id:
                    poem_interaction = db_session.query(PoemLike).filter(and_(
                        PoemLike.poem_id == poem.id,
                        PoemLike.user_id == user_id
                    )).first()
                    if poem_interaction:
                        is_liked_by_user = True
                obj = {
                    'id': poem.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id,
                    },
                    'title': poem.title,
                    'publishedOn': poem.created_on.isoformat(),
                    'verses': json.JSONDecoder().decode(poem.text),
                    'commentsCount': comments_count,
                    'likesCount': likes_count,
                    'isLiked': is_liked_by_user
                }
                user_poems.append(obj)
        user_poems.sort(
            key=lambda x: datetime.fromisoformat(x['publishedOn']),
            reverse=True
        )
        response = {
            'success': True,
            'data': extract_page(
                user_poems,
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


@router.get('/poems-user-likes')
async def get_liked_poems(userId, token='', span='', after='', before=''):
    '''Retrieves poems liked by a given user.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poems liked by the user.'
    }
    if not userId:
        return response
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        # sanitize span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        likes = db_session.query(PoemLike).filter(
            PoemLike.user_id == userId
        ).all()
        user_poems_liked = []
        for poem_like in likes:
            # retrieve information related to the current reaction
            poem = db_session.query(Poem).filter(
                Poem.id == poem_like.poem_id
            ).first()
            user = db_session.query(User).filter(
                User.id == poem.user_id
            ).first()
            comments = db_session.query(Comment).filter(and_(
                Comment.poem_id == poem.id,
                Comment.comment_id == None
            )).all()
            comments_count = len(comments) if comments else 0
            likes = db_session.query(PoemLike).filter(
                PoemLike.poem_id == poem.id
            ).all()
            likes_count = len(likes) if likes else 0
            is_liked_by_user = False
            if user_id != userId:
                poem_interaction = db_session.query(PoemLike).filter(and_(
                    PoemLike.poem_id == poem.id,
                    PoemLike.user_id == user_id
                )).first()
                if poem_interaction:
                    is_liked_by_user = True
            else:
                is_liked_by_user = True
            obj = {
                'id': poem.id,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id,
                },
                'title': poem.title,
                'publishedOn': poem.created_on.isoformat(),
                'verses': json.JSONDecoder().decode(poem.text),
                'commentsCount': comments_count,
                'likesCount': likes_count,
                'isLiked': is_liked_by_user
            }
            user_poems_liked.append(obj)
        user_poems_liked.sort(
            key=lambda x: datetime.fromisoformat(x['publishedOn'])
        )
        response = {
            'success': True,
            'data': extract_page(
                user_poems_liked,
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


@router.get('/poems-channel')
async def get_channel_poems(token, span='', after='', before=''):
    '''Retrieves poems for a user's timeline or home section.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poems for the channel.'
    }
    auth_token = AuthToken.decode(token)
    if auth_token is None:
        response['message'] = 'Invalid authentication token.'
        return response
    user_id = auth_token.user_id
    db_session = get_session()
    try:
        # sanitize span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        followings = db_session.query(UserFollowing).filter(
            UserFollowing.follower_id == user_id
        ).all()
        max_size = 2**32 - 1
        followings_count = len(followings) + 1 if followings else 1
        poems_per_following = max_size // followings_count
        poem_users_ids = [user_id]
        if followings:
            poem_users_ids.extend(list(map(lambda x: x.following_id, followings)))
        users_poems = []
        for id in poem_users_ids:
            # fetch poems_per_following poems for each following
            poems = db_session.query(Poem).filter(
                Poem.user_id == id
            ).limit(poems_per_following).all()
            user = db_session.query(User).filter(
                User.id == id
            ).first()
            for poem in poems:
                # retrieve information related to the current poem
                comments = db_session.query(Comment).filter(and_(
                    Comment.poem_id == poem.id,
                    Comment.comment_id == None
                )).all()
                comments_count = len(comments) if comments else 0
                likes = db_session.query(PoemLike).filter(
                    PoemLike.poem_id == poem.id
                ).all()
                likes_count = len(likes) if likes else 0
                is_liked_by_user = False
                if user_id:
                    poem_interaction = db_session.query(PoemLike).filter(and_(
                        PoemLike.poem_id == poem.id,
                        PoemLike.user_id == user_id
                    )).first()
                    if poem_interaction:
                        is_liked_by_user = True
                obj = {
                    'id': poem.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'title': poem.title,
                    'publishedOn': poem.created_on.isoformat(),
                    'verses': json.JSONDecoder().decode(poem.text),
                    'commentsCount': comments_count,
                    'likesCount': likes_count,
                    'isLiked': is_liked_by_user
                }
                users_poems.append(obj)
        # stable sort based on creation time
        users_poems.sort(
            key=lambda x: datetime.fromisoformat(x['publishedOn']),
            reverse=True
        )
        response = {
            'success': True,
            'data': extract_page(
                users_poems,
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


@router.get('/poems-explore')
async def get_exploratory_poems(token, span='', after='', before=''):
    '''Retrieves poems a user can explore.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poems for the user.'
    }
    auth_token = AuthToken.decode(token)
    if auth_token is None:
        response['message'] = 'Invalid authentication token.'
        return response
    user_id = auth_token.user_id if auth_token is not None else None
    db_session = get_session()
    try:
        # sanitize span
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        followings = db_session.query(UserFollowing).filter(
            UserFollowing.follower_id == user_id
        ).all()
        max_poems_count = 48
        poem_users_ids = [user_id]
        if followings:
            poem_users_ids.extend(
                list(map(lambda x: x.following_id, followings))
            )
        explore_poems = []
        # fetch max_poems_count for the user from people
        # the user isn't following
        poems = db_session.query(Poem).filter(
            Poem.user_id.notin_(poem_users_ids)
        ).limit(max_poems_count).all()
        for poem in poems:
            # retrieve information related to the current poem
            user = db_session.query(User).filter(
                User.id == poem.user_id
            ).first()
            comments = db_session.query(Comment).filter(and_(
                Comment.poem_id == poem.id,
                Comment.comment_id == None
            )).all()
            comments_count = len(comments) if comments else 0
            likes = db_session.query(PoemLike).filter(
                PoemLike.poem_id == poem.id
            ).all()
            likes_count = len(likes) if likes else 0
            is_liked_by_user = False
            if user_id:
                poem_interaction = db_session.query(PoemLike).filter(and_(
                    PoemLike.poem_id == poem.id,
                    PoemLike.user_id == user_id
                )).first()
                if poem_interaction:
                    is_liked_by_user = True
            obj = {
                'id': poem.id,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'profilePhotoId': user.profile_photo_id
                },
                'title': poem.title,
                'publishedOn': poem.created_on.isoformat(),
                'verses': json.JSONDecoder().decode(poem.text),
                'commentsCount': comments_count,
                'likesCount': likes_count,
                'isLiked': is_liked_by_user
            }
            explore_poems.append(obj)
        explore_poems.sort(
            key=lambda x: x['likesCount'],
            reverse=True
        )
        response = {
            'success': True,
            'data': extract_page(
                explore_poems,
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
