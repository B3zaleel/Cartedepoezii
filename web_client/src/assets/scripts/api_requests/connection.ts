import UserMin from '../types/user_min';

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
   * @param span - The maximum number of followers to retrieve.
   */
  getFollowers(userId: string, span = 12, after = '', before = ''):
    Promise<{success: boolean, data: Array<UserMin> | string} | Error> {
    const path = [
      this.BASE_URL,
      '/followers?',
      `id=${userId}`,
      span ? `&span${span <= 0 ? 12 : span}` : '',
      after ? `&after=${after}` : '',
      before ? `&before=${before}` : '',
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
   * @param span - The maximum number of followers to retrieve.
   */
  getFollowings(userId: string, span = 12, after = '', before = ''):
    Promise<{success: boolean, data: Array<UserMin> | string} | Error> {
    const path = [
      this.BASE_URL,
      '/followings?',
      `id=${userId}`,
      span ? `&span${span <= 0 ? 12 : span}` : '',
      after ? `&after=${after}` : '',
      before ? `&before=${before}` : '',
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
   * @param span - The maximum number of followers to retrieve.
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
