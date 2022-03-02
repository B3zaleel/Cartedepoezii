import { Item } from './interfaces';
import UserMin from './user_min';

export default class Comment implements Item {
  id!: string;

  user!: UserMin;

  poemId!: string;

  createdOn!: Date;

  text!: string;

  repliesTo!: string;

  repliesCount!: number;
}
