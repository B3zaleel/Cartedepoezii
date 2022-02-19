# Version 1 of Cartedepoezii's API Documentation

**BASE_URL:** `/api/v1`

## What You Should Know

A successful response from the API server should yield a response that looks like this:
```javascript
{
    success: Boolean, // will be true
    data: Object | Array
}
```
The `data` key above would contain the responses of the endpoints described below.

If there was an error with your response, you should get a response that looks like this:
```javascript
{
    success: Boolean, // will be false
    message: String
}
```

## Endpoints

### Authentication

`POST:` **{BASE_URL}***/sign-up*
<br/>Body
```javascript
{
    name: String,
    email: String,
    password: String
}
```
Response
```javascript
{
    userId: String,
    authToken: String
}
```

`POST:` **{BASE_URL}***/sign-in*
<br/>Body
```javascript
{
    email: String,
    password: String
}
```
Response
```javascript
{
    userId: String,
    authToken: String
}
```

`POST:` **{BASE_URL}***/reset-password*
<br/>Body
```javascript
{
    email: String
}
```
Response
```javascript
{}
```

`PUT:` **{BASE_URL}***/reset-password*
<br/>Body
```javascript
{
    email: String,
    password: String,
    resetToken: String
}
```
Response
```javascript
{
    authToken: String
}
```

### User

`GET:` **{BASE_URL}***/user?id&token*
<br/>Response
```javascript
{
    id: String,
    joined: String,
    name: String,
    bio: String,
    profilePhotoId: String,
    followersCount: Number,
    followingsCount: Number,
    isFollowing: Boolean
}
```

`PUT:` **{BASE_URL}***/user*
<br/>Body (as FormData)
```yaml
authToken: String
userId: str
name: String
profilePhoto: BLOB
removeProfilePhoto: Boolean
bio: String
email: String
```
Response
```javascript
{
    authToken: String,
    profilePhotoId: String
}
```

`DELETE:` **{BASE_URL}***/user*
<br/>Body
```javascript
{
    authToken: String,
    userId: String
}
```
Response
```javascript
{}
```

### Connection

`GET:` **{BASE_URL}***/followers?id&token&span&after&before*
<br/>Response
```javascript
[
    {
        id: String,
        name: String,
        profilePhotoId: String,
        isFollowing: Boolean
    }
    ...
]
```

`GET:` **{BASE_URL}***/followings?id&token&span&after&before*
<br/>Response
```javascript
[
    {
        id: String,
        name: String,
        profilePhotoId: String,
        isFollowing: Boolean
    }
    ...
]
```

`PUT:` **{BASE_URL}***/follow*
<br/>Body
```javascript
{
    authToken: String,
    userId: String,
    followId: String
}
```
Response
```javascript
{
    status: Boolean
}
```

### Poem

`GET:` **{BASE_URL}***/poem?id&token*
<br/>Response
```javascript
{
    authorId: String,
    authorName: String,
    authorprofilePhotoId: String,
    title: String,
    publishedDate: String,
    verses: Array<String>,
    commentsCount: Number,
    likesCount: Number,
    isLiked: Boolean
}
```

`POST:` **{BASE_URL}***/poem*
<br/>Body
```javascript
{
    authToken: String,
    userId: str,
    title: String,
    verses: Array<String>
}
```
Response
```javascript
{
    poemId: String
}
```

`PUT:` **{BASE_URL}***/poem*
<br/>Body
```javascript
{
    authToken: String,
    userId: str,
    title: String,
    verses: Array<String>
}
```
Response
```javascript
{}
```

`DELETE:` **{BASE_URL}***/poem*
<br/>Body
```javascript
{
    authToken: String,
    userId: String,
    poemId: String
}
```
Response
```javascript
{}
```

`GET:` **{BASE_URL}***/user-poems?userId&token&span&after&before*
<br/>Response
```javascript
[
    {
        authorId: String,
        authorName: String,
        authorprofilePhotoId: String,
        title: String,
        publishedDate: String,
        verses: Array<String>,
        commentsCount: Number,
        likesCount: Number,
        isLiked: Boolean
    }
    ...
]
```

`GET:` **{BASE_URL}***/poems-channel?token&span&after&before*
<br/>Response
```javascript
[
    {
        authorId: String,
        authorName: String,
        authorprofilePhotoId: String,
        title: String,
        publishedDate: String,
        verses: Array<String>,
        commentsCount: Number,
        likesCount: Number,
        isLiked: Boolean
    }
    ...
]
```

### Comment

`GET:` **{BASE_URL}***/poem-comments?id&token*
<br/>Response
```javascript
{
    commentId: String,
    userId: String,
    userName: String,
    userprofilePhotoId: String,
    createdOn: String,
    text: String,
    repliesTo: String,
    repliesCount: Number
}
```

`GET:` **{BASE_URL}***/poem-comments?id&token&span&after&before*
<br/>Response
```javascript
[
    {
        commentId: String,
        userId: String,
        userName: String,
        userprofilePhotoId: String,
        createdOn: String,
        text: String,
        repliesTo: String,
        repliesCount: Number
    }
    ...
]
```

`POST:` **{BASE_URL}***/poem-comments*
<br/>Body
```javascript
{
    authToken: String,
    userId: String,
    poemId: String,
    text: String,
    repliesTo: String // optional
}
```
Response
```javascript
{
    commentId: String,
    createdOn: String,
    repliesTo: String,
    repliesCount: Number
}
```

`DELETE:` **{BASE_URL}***/poem-comments*
<br/>Body
```javascript
{
    authToken: String,
    userId: String,
    commentId: String
}
```
Response
```javascript
{}
```

`GET:` **{BASE_URL}***/user-comments?token&span&after&before*
<br/>Response
```javascript
[
    {
        commentId: String,
        userId: String,
        userName: String,
        userprofilePhotoId: String,
        createdOn: String,
        text: String,
        repliesTo: String,
        repliesCount: Number
    }
    ...
]
```

### Search

`GET:` **{BASE_URL}***/search?q&token&type&span&after&before*
<br/>Response (type: *poems*)
```javascript
[
    {
        authorId: String,
        authorName: String,
        authorprofilePhotoId: String,
        title: String,
        publishedDate: String,
        verses: Array<String>,
        commentsCount: Number,
        likesCount: Number,
        isLiked: Boolean
    }
    ...
]
```
Response (type: *people*)
```javascript
[
    {
        userId: String,
        name: String,
        profilePhotoId: String,
        isFollowing: Boolean
    }
    ...
]
```

### Explore

TBD
