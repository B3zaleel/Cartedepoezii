import { Page } from '../types/interfaces';
import PoemMin from '../types/poem_min';
import PoemT from '../types/poem';

/**
 * Represents a class for handling poem-related API requests.
 */
export default class Poem {
  BASE_URL!: string;

  AUTH_TOKEN!: string;

  constructor(baseURL: string, authToken: string) {
    this.BASE_URL = baseURL;
    this.AUTH_TOKEN = authToken;
  }

  /**
   * Retrieve information about a poem.
   * @param poemId - The poem's id.
   */
  getPoem(poemId: string):
    Promise<{ success: boolean, data?: PoemT, message?: string }> {
    const path = [
      this.BASE_URL,
      '/poem?',
      `id=${poemId}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: PoemT, message?: string
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
   * Create a new poem.
   * @param userId - The id of user creating the poem.
   * @param title - The poem's title.
   * @param verses - The verses in the poem.
   */
  createPoem(userId: string, title: string, verses: Array<string>):
    Promise<{
      success: boolean,
      data?: { id: string, createdOn: string, repliesCount: number, likesCount: number },
      message?: string
    }> {
    const path = [
      this.BASE_URL,
      '/poem',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      title,
      verses,
    };
    const result = new Promise<{
      success: boolean,
      data?: { id: string, createdOn: string, repliesCount: number, likesCount: number },
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
   * Update an existing poem.
   * @param userId - The id of user creating the poem.
   * @param poemId - The id of the poem being edited.
   * @param title - The poem's title.
   * @param verses - The verses in the poem.
   */
  updatePoem(userId: string, poemId: string, title: string, verses: Array<string>):
    Promise<{
      success: boolean,
      data?: { id: string, createdOn: string, repliesCount: number, likesCount: number },
      message?: string
    }> {
    const path = [
      this.BASE_URL,
      '/poem',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      poemId,
      title,
      verses,
    };
    const result = new Promise<{
      success: boolean,
      data?: { id: string, createdOn: string, repliesCount: number, likesCount: number },
      message?: string
    }>((resolve, reject) => {
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

  /**
   * Remove a user's poem.
   * @param userId - The id of the user.
   * @param poemId - The id of the poem to remove.
   */
  deletePoem(userId: string, poemId: string):
    Promise<{ success: boolean, data?: Record<string, never>, message?: string }> {
    const path = [
      this.BASE_URL,
      '/poem',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      poemId,
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

  /**
   * Toggle a user's reaction on a poem.
   * @param userId - The id of the user.
   * @param poemId - The id of the poem to react on.
   */
  reactToPoem(userId: string, poemId: string):
    Promise<{ success: boolean, data?: { status: boolean }, message?: string }> {
    const path = [
      this.BASE_URL,
      '/like-poem',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId,
      poemId,
    };
    const result = new Promise<{
      success: boolean, data?: { status: boolean }, message?: string
    }>((resolve, reject) => {
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

  /**
   * Retrieve poems created by a given user.
   * @param userId - The user's id.
   */
  getPoemsUserCreated(userId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{ success: boolean, data?: Array<PoemMin>, message?: string }> {
    const path = [
      this.BASE_URL,
      '/poems-user-created?',
      `userId=${userId}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: Array<PoemMin>, message?: string
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
   * Retrieve poems liked by a given user.
   * @param userId - The user's id.
   */
  getPoemsUserLikes(userId: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{ success: boolean, data?: Array<PoemT>, message?: string }> {
    const path = [
      this.BASE_URL,
      '/poems-user-likes?',
      `userId=${userId}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: Array<PoemT>, message?: string
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
   * Retrieve poems for a user's timeline.
   */
  getPoemsForUser(page: Page = { span: 12, after: '', before: '' }):
    Promise<{ success: boolean, data?: Array<PoemT>, message?: string }> {
    const path = [
      this.BASE_URL,
      '/poems-channel?',
      `&token=${this.AUTH_TOKEN}`,
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: Array<PoemT>, message?: string
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
}
