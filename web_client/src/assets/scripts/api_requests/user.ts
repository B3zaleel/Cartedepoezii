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
    const bodyData = new FormData();
    bodyData.set('authToken', this.AUTH_TOKEN);
    bodyData.set('userId', updateForm.userId);
    bodyData.set('name', updateForm.name);
    if (updateForm.imageUploaded && !updateForm.removePhoto) {
      const mimeType = updateForm.imageURL.split(';')[0].split(':')[1];
      console.log(mimeType);
      bodyData.set('profilePhoto', new Blob(
        [updateForm.imageURL],
        { type: mimeType },
      ));
    }
    bodyData.set('profilePhotoId', updateForm.imageURL);
    bodyData.set('removeProfilePhoto', updateForm.removePhoto.toString());
    bodyData.set('email', updateForm.email);
    bodyData.set('bio', updateForm.bio);
    const result = new Promise<{
      success: boolean,
      data?: { authToken: string, profilePhotoId: string },
      message?: string
    }>((resolve, reject) => {
      fetch(path, {
        method: 'PUT',
        mode: 'cors',
        headers: {
          // 'Content-Type': 'application/json',
        },
        body: bodyData,
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
    const path = [
      this.BASE_URL,
      '/user?',
      `authToken=${this.AUTH_TOKEN}`,
      `&id=${userId}`,
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
      })
        .then((response) => resolve(response.json()))
        .catch((err) => reject(err));
    });
    return result;
  }
}
