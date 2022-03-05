import { Item } from './interfaces';
import UserMin from './user_min';

export default class Poem implements Item {
  id!: string;

  user!: UserMin;

  title!: string;

  publishedOn!: string;

  verses!: Array<string>;

  commentsCount!: number;

  likesCount!: number;

  isLiked!: boolean;

  constructor() {
    this.id = '';
    this.user = {
      id: '',
      name: '',
      profilePhotoId: '',
    };
    this.title = '';
    this.publishedOn = new Date().toISOString();
    this.verses = [''];
    this.commentsCount = 0;
    this.likesCount = 0;
    this.isLiked = false;
  }
}
