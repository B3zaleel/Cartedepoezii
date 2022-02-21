export interface User {
  id: string,
  name: string,
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

export interface Poem {
  id: string,
  user: User,
  title: string,
  publishedDate: Date,
  verses: Array<string>,
  commentsCount: number,
  likesCount: number,
  isLiked: boolean
}

export interface Comment {
  id: string,
  user: User,
  poem: Poem,
  createdDate: Date,
  text: string,
  repliesTo: string,
  repliesCount: number,
}
