import { EditProfileForm } from '../types/interfaces';
import UserT from '../types/user';

/**
 * Represents a class for handling user-related API requests.
 */
export default class User {
  BASE_URL!: string;

  AUTH_TOKEN!: string;

  constructor(baseURL: string, authToken: string) {
    this.BASE_URL = baseURL;
    this.AUTH_TOKEN = authToken;
  }

  /**
   * Retrieve a user's information.
   * @param userId - The user's id.
   */
  getUser(userId: string):
    Promise<{ success: boolean, data?: UserT, message?: string }> {
    const path = [
      this.BASE_URL,
      '/user?',
      `id=${userId}`,
      this.AUTH_TOKEN ? `&token=${this.AUTH_TOKEN}` : '',
    ].join('');
    const result = new Promise<{
      success: boolean, data?: UserT, message?: string
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
   * Retrieve profile photo of a user.
   * @param imgId - The id of the profile photo.
   */
  getProfilePhoto(imgId: string):
    Promise<{ success: boolean, data?: {url: string}, message?: string }> {
    const path = [
      this.BASE_URL,
      '/profile-photo?',
      `imgId=${imgId}`,
    ].join('');
    const result = new Promise<{
      success: boolean, data?: {url: string}, message?: string
    }>((resolve, reject) => {
      fetch(path, {
        method: 'GET',
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
   * Updates a user's information.
   * @param updateForm - The updateForm of the user.
   */
  updateUser(updateForm: EditProfileForm):
    Promise<{
      success: boolean,
      data?: { authToken: string, profilePhotoId: string },
      message?: string
    }> {
    const path = [
      this.BASE_URL,
      '/user',
    ].join('');
    const bodyData = {
      authToken: this.AUTH_TOKEN,
      userId: updateForm.userId,
      name: updateForm.name,
      profilePhoto: '',
      profilePhotoId: updateForm.imageURL,
      removeProfilePhoto: updateForm.removePhoto,
      email: updateForm.email,
      bio: updateForm.bio,
    };
    if (updateForm.imageUploaded && !updateForm.removePhoto) {
      bodyData.profilePhoto = updateForm.imageURL;
    }
    const result = new Promise<{
      success: boolean,
      data?: { authToken: string, profilePhotoId: string },
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
   * Removes a user's account.
   * @param userId - The id of the user.
   */
  deleteUser(userId: string):
    Promise<{ success: boolean, data?: Record<string, never>, message?: string }> {
    const bodyData = {
      userId,
      authToken: this.AUTH_TOKEN,
    };
    const path = [
      this.BASE_URL,
      '/user',
    ].join('');
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
