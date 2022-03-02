import { Item } from './interfaces';

export default class PoemMin implements Item {
  id!: string;

  title!: string;

  publishedOn!: string;

  verses!: Array<string>;

  commentsCount!: number;

  likesCount!: number;

  isLiked!: boolean
}
