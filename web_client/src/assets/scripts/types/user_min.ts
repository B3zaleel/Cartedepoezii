import { Item } from './interfaces';

export default class UserMin implements Item {
  id!: string;

  name!: string;

  profilePhotoId!: string;

  isFollowing?: boolean;
}
