#!/usr/bin/python3
import re
import uuid
from datetime import datetime
from fastapi import APIRouter
from sqlalchemy import and_

from ..form_types import CommentAddForm, CommentDeleteForm
from ..database import get_session, User, Comment
from ..utils.token_handlers import AuthToken
from ..utils.pagination import extract_page


router = APIRouter(prefix='/api/v1')


@router.get('/comment')
async def get_comment(id=''):
    response = {
        'success': False,
        'message': 'Failed to find comment.'
    }
    db_session = get_session()
    try:
        comment = db_session.query(Comment).filter(
            Comment.id == id
        ).first()
        if comment:
            user = db_session.query(User).filter(
                User.id == comment.user_id
            ).first()
            if not user:
                return response
            replies = db_session.query(Comment).filter(
                Comment.comment_id == comment.id,
            ).all()
            replies_count = len(replies) if replies else 0
            response = {
                'success': True,
                'data': {
                    'id': comment.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'createdOn': comment.created_on.isoformat(),
                    'text': comment.text,
                    'poemId': comment.poem_id,
                    'repliesCount': replies_count,
                    'replyTo': comment.comment_id if comment.comment_id else ''
                }
            }
    finally:
        db_session.close()
    return response


@router.get('/comments-of-poem')
async def get_poem_comments(id='', span='', after='', before=''):
    response = {
        'success': False,
        'message': 'Failed to find comments.'
    }
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
        comments = db_session.query(Comment).filter(and_(
            Comment.poem_id == id,
            Comment.comment_id == None
        )).all()
        new_comments = []
        if comments:
            for comment in comments:
                user = db_session.query(User).filter(
                    User.id == comment.user_id
                ).first()
                if not user:
                    continue
                replies = db_session.query(Comment).filter(and_(
                    Comment.poem_id == id,
                    Comment.comment_id == comment.id,
                )).all()
                replies_count = len(replies) if replies else 0
                obj = {
                    'id': comment.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'createdOn': comment.created_on.isoformat(),
                    'text': comment.text,
                    'poemId': comment.poem_id,
                    'repliesCount': replies_count,
                    'replyTo': comment.comment_id if comment.comment_id else ''
                }
                new_comments.append(obj)
        new_comments.sort(
            key=lambda x: datetime.fromisoformat(x['createdOn'])
        )
        response = {
            'success': True,
            'data': extract_page(
                new_comments,
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


@router.get('/comment-replies')
async def get_comment_replies(id='', span='', after='', before=''):
    response = {
        'success': False,
        'message': 'Failed to find replies to comment.'
    }
    if not id:
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
        comments = db_session.query(Comment).filter(
            Comment.comment_id == id
        ).all()
        new_replies = []
        if comments:
            for comment in comments:
                user = db_session.query(User).filter(
                    User.id == comment.user_id
                ).first()
                if not user:
                    continue
                replies = db_session.query(Comment).filter(and_(
                    Comment.poem_id == id,
                    Comment.comment_id == comment.id,
                )).all()
                replies_count = len(replies) if replies else 0
                obj = {
                    'id': comment.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'createdOn': comment.created_on.isoformat(),
                    'text': comment.text,
                    'poemId': comment.poem_id,
                    'repliesCount': replies_count,
                    'replyTo': comment.comment_id if comment.comment_id else ''
                }
                new_replies.append(obj)
        new_replies.sort(
            key=lambda x: datetime.fromisoformat(x['createdOn'])
        )
        response = {
            'success': True,
            'data': extract_page(
                new_replies,
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


@router.get('/comments-by-user')
async def get_comments_by_user(id='', span='', after='', before=''):
    response = {
        'success': False,
        'message': 'User id is required.'
    }
    if not id:
        return response
    response = {
        'success': False,
        'message': 'Failed to find comments.'
    }
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
        user = db_session.query(User).filter(User.id == id).first()
        if not user:
            return response
        comments = db_session.query(Comment).filter(
            Comment.user_id == id
        ).all()
        new_comments = []
        if comments:
            for comment in comments:
                replies = db_session.query(Comment).filter(
                    Comment.comment_id == comment.id
                ).all()
                replies_count = len(replies) if replies else 0
                obj = {
                    'id': comment.id,
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'profilePhotoId': user.profile_photo_id
                    },
                    'createdOn': comment.created_on.isoformat(),
                    'text': comment.text,
                    'poemId': comment.poem_id,
                    'replyTo': comment.comment_id if comment.comment_id else '',
                    'repliesCount': replies_count
                }
                new_comments.append(obj)
        new_comments.sort(
            key=lambda x: datetime.fromisoformat(x['createdOn'])
        )
        response = {
            'success': True,
            'data': extract_page(
                new_comments,
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


@router.post('/comment')
async def add_comment(body: CommentAddForm):
    response = {
        'success': False,
        'message': 'Failed to add comment.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    if len(body.text) > 384:
        response['message'] = 'Name is too long.'
        return response
    db_session = get_session()
    try:
        replyId = body.replyTo.strip() if body.replyTo else None
        if replyId:
            result = db_session.query(Comment).filter(and_(
                Comment.id == replyId,
                Comment.comment_id == None
            )).first()
            if not result or result.poem_id != body.poemId:
                db_session.close()
                return response
        gen_id = str(uuid.uuid4())
        cur_time = datetime.utcnow()
        comment = Comment(
            id=gen_id,
            created_on=cur_time,
            poem_id=body.poemId,
            user_id=body.userId,
            comment_id=replyId,
            text=body.text,
        )
        db_session.add(comment)
        db_session.commit()
        response = {
            'success': True,
            'data': {
                'id': gen_id,
                'createdOn': cur_time.isoformat(),
                'replyTo': body.replyTo if body.replyTo else '',
                'poemId': body.poemId,
                'repliesCount': 0
            }
        }
    except Exception as ex:
        print(ex.args[0])
        db_session.rollback()
    finally:
        db_session.close()
    return response


@router.delete('/comment')
async def remove_comment(body: CommentDeleteForm):
    response = {
        'success': False,
        'message': 'Failed to remove comment.'
    }
    auth_token = AuthToken.decode(body.authToken)
    if auth_token is None or auth_token.user_id != body.userId:
        response['message'] = 'Invalid authentication token.'
        return response
    db_session = get_session()
    try:
        db_session.query(Comment).filter(
            Comment.comment_id == body.commentId,
        ).delete(
            synchronize_session=False
        )
        db_session.query(Comment).filter(
            Comment.id == body.commentId,
        ).delete(
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
