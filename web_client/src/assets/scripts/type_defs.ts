export interface User {
  id: string,
  name: string,
  email: string,
  bio: string,
  joinDate: Date,
  profilePhotoId: string,
  followersCount: number,
  followingsCount: number,
  poemsCount: number,
  commentsCount: number,
  likesCount: number,
  isFollowing: boolean,
}

export interface UserMin {
  id: string,
  name: string,
  profilePhotoId: string,
  isFollowing: boolean,
}

export interface Poem {
  id: string,
  user: UserMin,
  title: string,
  publishedDate: Date,
  verses: Array<string>,
  commentsCount: number,
  likesCount: number,
  isLiked: boolean
}

export interface Comment {
  id: string,
  user: UserMin,
  poemId: string,
  createdDate: Date,
  text: string,
  repliesTo: string,
  repliesCount: number,
}

export interface FileInputEvent {
  target: HTMLInputElement
}

export interface ElementInputEvent {
  target: HTMLElement
}
