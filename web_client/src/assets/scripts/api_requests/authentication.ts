/**
 * Represents a class for handling authentication-related API calls.
 */
export default class Authentication {
  BASE_URL!: string;

  constructor(baseURL: string) {
    this.BASE_URL = baseURL;
  }

  /**
   * Authenticate an existing user.
   * @param email - The user's email.
   * @param password - The user's password.
   */
  signIn(email: string, password: string):
    Promise<{
      success: boolean,
      data?: { userId: string, name: string, authToken: string },
      message?: boolean
    }> {
    const path = [
      this.BASE_URL,
      '/sign-in',
    ].join('');
    const bodyData = {
      email,
      password,
    };
    const result = new Promise<{
      success: boolean,
      data?: { userId: string, name: string, authToken: string },
      message?: boolean
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
   * Create a new user.
   * @param name - The user's name.
   * @param email - The user's email.
   * @param password - The user's password.
   */
  signUp(name: string, email: string, password: string):
    Promise<{
      success: boolean,
      data?: { userId: string, name: string, authToken: string },
      message?: boolean
    }> {
    const path = [
      this.BASE_URL,
      '/sign-up',
    ].join('');
    const bodyData = {
      name,
      email,
      password,
    };
    const result = new Promise<{
      success: boolean,
      data?: { userId: string, name: string, authToken: string },
      message?: boolean
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
   * Request a password reset token for the given user.
   * @param email - The user's email.
   */
  requestResetPassword(email: string):
    Promise<{
      success: boolean,
      data?: Record<string, never>,
      message?: boolean
    }> {
    const path = [
      this.BASE_URL,
      '/reset-password',
    ].join('');
    const bodyData = {
      email,
    };
    const result = new Promise<{
      success: boolean,
      data?: Record<string, never>,
      message?: boolean
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
   * Reset a user's password.
   * @param userId - The user's id.
   * @param email - The user's email.
   * @param password - The user's new password.
   * @param resetToken - The user's password reset token.
   */
  resetPassword(userId: string, email: string, password: string, resetToken: string):
    Promise<{
      success: boolean,
      data?: Record<string, never>,
      message?: boolean
    }> {
    const path = [
      this.BASE_URL,
      '/reset-password',
    ].join('');
    const bodyData = {
      email,
      password,
      resetToken,
    };
    const result = new Promise<{
      success: boolean,
      data?: Record<string, never>,
      message?: boolean
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
}
