import { Item } from './interfaces';

export default class User implements Item {
  id!: string;

  name!: string;

  email!: string;

  bio!: string;

  joined!: string;

  profilePhotoId!: string;

  followersCount!: number;

  followingsCount!: number;

  poemsCount!: number;

  commentsCount!: number;

  likesCount!: number;

  isFollowing!: boolean;

  constructor() {
    this.id = '';
    this.name = '';
    this.email = '';
    this.bio = '';
    this.joined = new Date().toISOString();
    this.profilePhotoId = '';
    this.followersCount = 0;
    this.followingsCount = 0;
    this.poemsCount = 0;
    this.commentsCount = 0;
    this.likesCount = 0;
    this.isFollowing = false;
  }
}
