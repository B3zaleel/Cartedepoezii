import UserMin from '../types/user_min';
import { Page } from '../types/interfaces';

/**
 * Represents a class for handling connection-related API calls.
 */
export default class Connection {
  BASE_URL!: string;

  AUTH_TOKEN!: string;

  constructor(baseURL: string, authToken: string) {
    this.BASE_URL = baseURL;
    this.AUTH_TOKEN = authToken;
  }

  /**
   * Retrieve the followers of the given user.
   * @param userId - The id of the user.
   * @param page - The page of results to retrieve.
   */
  getFollowers(userId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{success: boolean, data: Array<UserMin> | string} | Error> {
    const path = [
      this.BASE_URL,
      '/followers?',
      `id=${userId}`,
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data: Array<UserMin>
      } | Error>(
        (resolve, reject) => {
          fetch(path, {
            method: 'PUT',
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
   * Retrieve the users followed by the given user.
   * @param userId - The id of the user.
   * @param page - The page of results to retrieve.
   */
  getFollowings(userId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{success: boolean, data: Array<UserMin> | string} | Error> {
    const path = [
      this.BASE_URL,
      '/followings?',
      `id=${userId}`,
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data: Array<UserMin>
      } | Error>((resolve, reject) => {
        fetch(path, {
          method: 'PUT',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then((response) => resolve(response.json()))
          .catch((err) => reject(err));
      });
    return result;
  }

  /**
   * Toggle the connection between two users.
   * @param userId - The id of the user.
   * @param followId - The id of the other user.
   */
  follow(userId: string, followId: string):
    Promise<{success: boolean, data: {status: boolean}} | Error> {
    const path = [
      this.BASE_URL,
      '/follow',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      followId,
    };
    const result = new Promise<{
      success: boolean, data: {status: boolean}
      } | Error>((resolve, reject) => {
        fetch(path, {
          method: 'PUT',
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
