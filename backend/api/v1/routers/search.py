#!/usr/bin/python3
import json
import re
from fastapi import APIRouter
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from typing import List

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


def get_unique_poems(
    poems: List[Poem],
    poems_seen: List[str],
    db_session,
    user_id):
    '''Retrieves a list of unique poems from a list of poems.
    '''
    results = []
    for poem in poems:
        if poem.id in poems_seen:
            continue
        poems_seen.append(poem.id)
        user = db_session.query(
            User).filter(
                User.id == poem.user_id).first()
        if not user:
            continue
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
            poem_interaction = db_session.query(
                PoemLike).filter(and_(
                    PoemLike.poem_id == poem.id,
                    PoemLike.user_id == user_id
                )).first()
            if poem_interaction:
                is_liked_by_user = True
        obj = {
            'user': {
                'id': user.id,
                'name': user.name,
                'profilePhotoId': user.profile_photo_id,
            },
            'id': poem.id,
            'title': poem.title,
            'publishedOn': poem.created_on.isoformat(),
            'verses': json.JSONDecoder().decode(poem.text),
            'commentsCount': comments_count,
            'likesCount': likes_count,
            'isLiked': is_liked_by_user
        }
        results.append(obj)
    return results


def get_unique_users(
    users: List[User],
    users_seen: List[str],
    db_session,
    user_id):
    '''Retrieves a list of unique users from a list of users.
    '''
    results = []
    for user in users:
        if user.id in users_seen:
            continue
        users_seen.append(user.id)
        is_following = False
        if user_id:
            user_connection = db_session.query(
                UserFollowing).filter(and_(
                    UserFollowing.follower_id == user_id,
                    UserFollowing.following_id == user.id
                )).first()
            if user_connection:
                is_following = True
        obj = {
            'id': user.id,
            'name': user.name,
            'profilePhotoId': user.profile_photo_id,
            'isFollowing': is_following
        }
        results.append(obj)
    return results


@router.get('/search-poems')
async def find_poems(q='', token='', span='', after='', before=''):
    '''Retrieves a list of poems that match a given query.
    '''
    response = {
        'success': False,
        'message': 'Failed to find poems.'
    }
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
            return response
        span = int(span if span else '12')
        query = q.replace('"', '')
        query = query.replace('\'', '').strip()
        if not query:
            return response
        query = "'{}'".format(query.strip())
        text_search_results = db_session.query(Poem).filter(
            Poem.__ts_text_vector__.match(
                query,
                postgresql_regconfig='english'
            )
        ).all()
        title_search_results = db_session.query(Poem).filter(
            Poem.__ts_title_vector__.match(
                query,
                postgresql_regconfig='english'
            )
        ).all()
        new_result = []
        poems_seen_ids = []
        if text_search_results:
            new_result.extend(
                get_unique_poems(
                    text_search_results,
                    poems_seen_ids,
                    db_session,
                    user_id
                )
            )
        if title_search_results:
            new_result.extend(
                get_unique_poems(
                    title_search_results,
                    poems_seen_ids,
                    db_session,
                    user_id
                )
            )
        response = {
            'success': True,
            'data': extract_page(
                new_result,
                span,
                after,
                before,
                True,
                lambda x: x['id']
            )
        }
    except SQLAlchemyError:
        response = {
            'success': False,
            'message': 'Invalid search query.'
        }
    finally:
        db_session.close()
    return response


@router.get('/search-people')
async def find_users(q='', token='', span='', after='', before=''):
    '''Retrieves a list of users that match a given query.
    '''
    response = {
        'success': False,
        'message': 'Failed to find users.'
    }
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
        query = q.replace('"', '')
        query = query.replace('\'', '').strip()
        if not query:
            return response
        query = "'{}'".format(query.strip())
        name_search_results = db_session.query(User).filter(
            User.__ts_name_vector__.match(
                query,
                postgresql_regconfig='english'
            )
        ).all()
        bio_search_results = db_session.query(User).filter(
            User.__ts_bio_vector__.match(
                query,
                postgresql_regconfig='english'
            )
        ).all()
        bio_search_results = []
        new_result = []
        users_seen_ids = []
        if name_search_results:
            new_result.extend(
                get_unique_users(
                    name_search_results,
                    users_seen_ids,
                    db_session,
                    user_id
                )
            )
        if bio_search_results:
            new_result.extend(
                get_unique_users(
                    bio_search_results,
                    users_seen_ids,
                    db_session,
                    user_id
                )
            )
        response = {
            'success': True,
            'data': extract_page(
                new_result,
                span,
                after,
                before,
                True,
                lambda x: x['id']
            )
        }
    except SQLAlchemyError:
        response = {
            'success': False,
            'message': 'Invalid search query.'
        }
    finally:
        db_session.close()
    return response
