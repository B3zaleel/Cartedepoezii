import { Item } from './interfaces';
import UserMin from './user_min';

export default class Poem implements Item {
  id!: string;

  user!: UserMin;

  title!: string;

  publishedOn!: Date;

  verses!: Array<string>;

  commentsCount!: number;

  likesCount!: number;

  isLiked!: boolean
}
