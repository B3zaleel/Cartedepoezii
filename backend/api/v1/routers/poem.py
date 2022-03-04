#!/usr/bin/python3
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
            user = db_session.query(User).filter(
                User.id == poem.user_id
            ).first()
            if not user:
                return response
            comments = db_session.query(Comment).filter(
                Comment.poem_id == id
            ).all()
            comments_count = len(comments) if comments else 0
            likes = db_session.query(PoemLike).filter(
                PoemLike.poem_id == id
            ).all()
            likes_count = len(likes) if likes else 0
            is_liked_by_user = False
            if user_id:
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
    response = {
        'success': False,
        'message': 'Failed to add poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    wrong_conditions = [
        auth_token is None,
        auth_token is not None and (auth_token.user_id != body.userId),
        len(body.title) > 256,
        len(body.verses) < 1,
        not all(list(map(lambda x: len(x.strip()) > 1, body.verses)))
    ]
    if any(wrong_conditions):
        return response
    db_session = get_session()
    try:
        gen_id = str(uuid.uuid4())
        cur_time = datetime.utcnow()
        adjusted_verses = []
        txt_fill = '\n\xa0'
        trimmed_verses = map(lambda x: x.strip(), body.verses)
        max_line = max(map(lambda x: x.count('\n'), trimmed_verses))
        for verse in trimmed_verses:
            new_verse = '{}{}'.format(verse, txt_fill * (max_line - verse.count('\n')))
            adjusted_verses.append(new_verse)
        poem = Poem(
            id=gen_id,
            created_on=cur_time,
            updated_on=cur_time,
            user_id=body.userId,
            title=body.title,
            text=json.JSONEncoder().encode(adjusted_verses)
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
    response = {
        'success': False,
        'message': 'Failed to update poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    wrong_conditions = [
        auth_token is None,
        auth_token is not None and (auth_token.user_id != body.userId),
        len(body.title) > 256,
        len(body.verses) < 1,
        not all(list(map(lambda x: len(x.strip()) > 1, body.verses)))
    ]
    if any(wrong_conditions):
        return response
    db_session = get_session()
    try:
        cur_time = datetime.utcnow()
        adjusted_verses = []
        txt_fill = '\n\xa0'
        trimmed_verses = map(lambda x: x.strip(), body.verses)
        max_line = max(map(lambda x: x.count('\n'), trimmed_verses))
        for verse in trimmed_verses:
            new_verse = '{}{}'.format(verse, txt_fill * (max_line - verse.count('\n')))
            adjusted_verses.append(new_verse)
        db_session.query(Poem).filter(Poem.id == body.poemId).update(
            {
                Poem.title: body.title,
                Poem.updated_on: cur_time,
                Poem.text: json.JSONEncoder().encode(adjusted_verses)
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
    response = {
        'success': False,
        'message': 'Failed to remove poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        return response
    db_session = get_session()
    try:
        db_session.query(Poem).filter(and_(
            Poem.poem_id == body.poemId,
            Poem.user_id == body.userId,
        )).delete(
            synchronize_session=False
        )
        db_session.query(Comment).filter(and_(
            Comment.poem_id == body.poemId,
            Comment.id == body.commentId,
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
    response = {
        'success': False,
        'message': 'Failed to like poem.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or (auth_token.user_id != body.userId):
        return response
    db_session = get_session()
    try:
        cur_usr_fav = db_session.query(PoemLike).filter(and_(
            PoemLike.user_id == auth_token.user_id,
            PoemLike.poem_id == body.poemId,
        )).first()
        if cur_usr_fav:
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
        span = span.strip()
        if span and re.fullmatch(r'\d+', span) is None:
            response = {
                'success': False,
                'message': 'Invalid span type.'
            }
            db_session.close()
            return response
        span = int(span if span else '12')
        result = db_session.query(Poem).filter(
            Poem.user_id == userId
        ).all()
        user_poems = []
        if result is not None:
            user = db_session.query(User).filter(
                User.id == userId
            ).first()
            if not user:
                return response
            for item in result:
                comments = db_session.query(Comment).filter(
                    Comment.poem_id == item.id
                ).all()
                comments_count = len(comments) if comments else 0
                likes = db_session.query(PoemLike).filter(
                    PoemLike.poem_id == item.id
                ).all()
                likes_count = len(likes) if likes else 0
                is_liked_by_user = False
                if user_id:
                    poem_interaction = db_session.query(PoemLike).filter(and_(
                        PoemLike.poem_id == item.id,
                        PoemLike.user_id == user_id
                    )).first()
                    if poem_interaction:
                        is_liked_by_user = True
                obj = {
                    'id': item.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id,
                    },
                    'title': item.title,
                    'publishedOn': item.created_on.isoformat(),
                    'verses': json.JSONDecoder().decode(item.text),
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
    response = {
        'success': False,
        'message': 'Failed to find poems for the channel.'
    }
    if not token:
        return response
    auth_token = AuthToken.decode(token)
    user_id = auth_token.user_id if auth_token is not None else None
    if not user_id:
        return response
    db_session = get_session()
    try:
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
        m = len(followings) + 1 if followings else 1
        n = max_size // m
        poem_users_ids = [user_id]
        if followings:
            poem_users_ids.extend(list(map(lambda x: x.following_id, followings)))
        users_poems = []
        for id in poem_users_ids:
            poems = db_session.query(Poem).filter(
                Poem.user_id == id
            ).limit(n).all()
            user = db_session.query(User).filter(
                User.id == id
            ).first()
            for poem in poems:
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
