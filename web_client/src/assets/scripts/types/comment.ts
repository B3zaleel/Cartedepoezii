import { Item } from './interfaces';
import UserMin from './user_min';

export default class Comment implements Item {
  id!: string;

  user?: UserMin;

  poemId!: string;

  createdOn!: string;

  text!: string;

  replyTo!: string;

  repliesCount!: number;
}
