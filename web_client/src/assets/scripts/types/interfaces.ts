export interface Item {
  id: string;
}

export interface Page {
  span: number;
  after: string;
  before: string;
}

export interface FileInputEvent {
  target: HTMLInputElement
}

export interface ElementInputEvent {
  target: HTMLElement
}

export interface EditProfileForm {
  imageURL: string;
  imageUploaded: boolean;
  removePhoto: boolean;
  email: string;
  name: string;
  bio: string;
}
