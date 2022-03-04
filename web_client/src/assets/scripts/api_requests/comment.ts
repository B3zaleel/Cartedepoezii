import { Page } from '../types/interfaces';
import UserMin from '../types/user_min';
import CommentT from '../types/comment';

/**
 * Represents a class for handling comment-related API requests.
 */
export default class Comment {
  BASE_URL!: string;

  AUTH_TOKEN!: string;

  constructor(baseURL: string, authToken: string) {
    this.BASE_URL = baseURL;
    this.AUTH_TOKEN = authToken;
  }

  /**
   * Retrieve comments on a poem.
   * @param poemId - The poem's id.
   */
  getPoemComments(poemId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{ success: boolean, data: Array<CommentT> }> {
    const path = [
      this.BASE_URL,
      '/comments?',
      `id=${poemId}`,
      page.span ? `&span=${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data: Array<CommentT>
    }>(
      (resolve, reject) => {
        fetch(path, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => resolve(response.json()))
          .catch((err) => reject(err));
      },
    );
    return result;
  }

  /**
   * Retrieve replies to a comment.
   * @param poemId - The poem's id.
   */
  getCommentReplies(commentId: string, poemId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{ success: boolean, data: Array<CommentT> }> {
    const path = [
      this.BASE_URL,
      '/comment-replies?',
      `id=${commentId}`,
      `&poemId=${poemId}`,
      page.span ? `&span=${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data: Array<CommentT>
    }>(
      (resolve, reject) => {
        fetch(path, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => resolve(response.json()))
          .catch((err) => reject(err));
      },
    );
    return result;
  }

  /**
   * Retrieve comments made by a user.
   * @param userId - The user's id.
   */
  getCommentsByUser(userId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{
      success: boolean,
      data?: {user: UserMin, comments: Array<CommentT>},
      message?: string
    }> {
    const path = [
      this.BASE_URL,
      '/comments-by-user?',
      `id=${userId}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
      page.span ? `&span=${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean,
      data?: {user: UserMin, comments: Array<CommentT>},
      message?: string
    }>(
      (resolve, reject) => {
        fetch(path, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => resolve(response.json()))
          .catch((err) => reject(err));
      },
    );
    return result;
  }

  /**
   * Create a new comment.
   * @param poemId - The id of the poem being commented under.
   * @param userId - The id of user commenting.
   * @param text - The comment's content.
   * @param replyTo - The id of the comment being replied to.
   */
  createComment(poemId: string, userId: string, text: string, replyTo = ''):
    Promise<{
      success: boolean,
      data?: CommentT,
      message?: string
    }> {
    const path = [
      this.BASE_URL,
      '/comments',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      poemId,
      text,
      replyTo,
    };
    const result = new Promise<{
      success: boolean,
      data?: CommentT,
      message?: string
    }>((resolve, reject) => {
      fetch(path, {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bodyData),
      })
        .then((response) => resolve(response.json()))
        .catch((err) => reject(err));
    });
    return result;
  }

  /**
   * Remove a user's comment.
   * @param userId - The id of the user.
   * @param poemId - The id of the poem the comment was made under.
   * @param commentId - The id of the comment to delete.
   */
  deleteComment(userId: string, poemId: string, commentId: string):
    Promise<{ success: boolean, data?: Record<string, never>, message?: string }> {
    const path = [
      this.BASE_URL,
      '/comments',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      poemId,
      commentId,
    };
    const result = new Promise<{
      success: boolean, data?: Record<string, never>, message?: string
    }>((resolve, reject) => {
      fetch(path, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bodyData),
      })
        .then((response) => resolve(response.json()))
        .catch((err) => reject(err));
    });
    return result;
  }
}
