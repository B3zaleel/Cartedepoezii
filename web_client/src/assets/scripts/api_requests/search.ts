import { Page } from '../types/interfaces';
import UserMin from '../types/user_min';
import Poem from '../types/poem';

/**
 * Represents a class for handling search-related API calls.
 */
export default class Search {
  BASE_URL!: string;

  AUTH_TOKEN!: string;

  constructor(baseURL: string, authToken: string) {
    this.BASE_URL = baseURL;
    this.AUTH_TOKEN = authToken;
  }

  /**
   * Retrieve people that match a given query.
   * @param query - The people search query.
   * @param page - The page of results to retrieve.
   */
  findPeople(query: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{success: boolean, data?: Array<UserMin>, message?: string}> {
    const path = [
      this.BASE_URL,
      '/search-people?',
      `q=${query}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: Array<UserMin>, message?: string
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
   * Retrieve poems that match a given query.
   * @param query - The poems search query.
   * @param page - The page of results to retrieve.
   */
  findPoems(query: string, page: Page = { span: 12, after: '', before: '' }):
    Promise<{success: boolean, data?: Array<Poem>, message?: string}> {
    const path = [
      this.BASE_URL,
      '/search-poems?',
      `q=${query}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
      page.span ? `&span${page.span <= 0 ? 12 : page.span}` : '',
      page.after ? `&after=${page.after}` : '',
      page.before ? `&before=${page.before}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: Array<Poem>, message?: string
      }>((resolve, reject) => {
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
}
