# notesapp
A web application that keeps a record of users' notes.
# requirements

### User account registration
Create a user account. These credentials will be used to log into this panel.

```js
[POST] /app/user

Request Data: { 'username': str,
                'password': str }

Response Data: { 'status': 'account created' }
```

### User account login:
Provide the ability to log into the panel using the user credentials.
```js
[POST] /app/user/auth

Request Data: { 'username': str,
                'password': str }

Response Data: { 'status': 'success', 'userId': int }
```
### List Saved Notes:
Provide list of stored notes for the logged-in user
```js
[GET] /app/sites/list/?user={userId}

Request Data: None 

Response Data: [List of saved notes]
```
### Save a new note:
Provide the ability for users to add a new note.
```js
[POST] /app/sites?user={userId}

Request Data: { 'note': str, }

Response Data: { 'status': 'success' } 
```

> Additional requirement : All the notes and passwords stored in the database are encrypted
