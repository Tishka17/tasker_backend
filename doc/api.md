## API Endpoints

### Base info

Base url for all requests is `/api/v1`
To get access token see authorization endpoint.

 
To use any api method (except authorization) you should send `Authorization` with access token. E.g.
```
Authorization: Bearer deadbeef
```

All responses consist of json with `error` or `data` field.
If there is no errors, requested object (or list of objects) is returned in `data` field. 


### Authorization

#### login+password
`**POST** /auth/login`

**In** (x-www-form-urlencoded):
* login - login as in set in user profile
* password - password and was set by user

**Out** (json):
```json
{
  "access_token": "your access token"
}
```

### vk.com
To get code from vk you should open a page with url: `https://oauth.vk.com/authorize?client_id={{client_id}}&response_type=code&redirect_uri={{redirect_url}}`
And then wait for opening redirect_uri with code in url params.

Client id and redirect url should be requested from current site author.

`**POST** /auth/vk`

**In**:
* code, returned by vk

**Out** (json):
```json
{
  "access_token": "your access token"
}
```

### Types

* Datetime is provided in iso format
* Visibility is enum with values: `full`, `title_only`, `presence_only`, `invisible`
* Priority is enum with values: `low`, `medium`, `high`


### User
User object, returned from server is json with these fields:
```json
{
      "about": null, 
      "blocked": false, 
      "confirmed": true, 
      "id": 1, 
      "login": "root", 
      "name": null, 
      "public_visibility": "invisible", 
      "registration_date": "2018-01-04T20:49:23", 
      "subscribers_visibility": "invisible"
}
```

#### List of users
`**GET** /users`
Out: array of user objects

#### User info
`**GET** /users/user_id`
`**GET** /users/self`
Out: user info

#### Update user info
`**PUT** /users/self`
In: json with user object
Out: updated user object

Only these fields can be updated:
* login
* name
* about
* subscribers_visibility
* public_visibility

#### Get user tasks
`**GET** /users/user_id/tasks`
`**GET** /users/self/tasks`
Out: array of user tasks (can be empty if user has now tasks)

### Tasks

Task is json with these fields.
```json
{
      "creation_date": "2018-01-04T21:27:55", 
      "deadline": "2018-12-17T11:01:55", 
      "description": "Some Desc 2", 
      "id": 1, 
      "modification_date": "2018-01-04T21:27:58", 
      "owner": <user object>, 
      "percent_progress": null, 
      "priority": "medium", 
      "public_visibility": "invisible", 
      "state": "finished", 
      "subscribers_visibility": "presence_only", 
      "title": "Some Title 2 "
    }
```

#### Create new task
`**POST** /tasks"`
In: json with task object
Out: json with created task object

Only these fields are should be provided:
* title
* description
* deadline (datetime, see types)
* priority (enum, see types)
* public_visibility
* subscribers_visibility

#### Get List of tasks
`**GET** /tasks/"`
Out: array of task objects


#### Get task by id
`**GET** /tasks/task_id"`
Out: task object

#### Update task by id
`**PUT** /tasks/task_id"`
In: json with task object
Out: json with updated task object

Only some fields can be updated. See creating new task

#### Delete task by id
`**DELETE** /tasks/task_id"`
Out: empty object

#### Update task state
`**PUT** /tasks/task_id/start"`
Out: json with updated task object

`**PUT** /tasks/task_id/pause"`
Out: json with updated task object

`**PUT** /tasks/task_id/finish"`
Out: json with updated task object

#### Create task reminder by task id
`**POST** /tasks/task_id/remind"`
In: json with reminder object
Out: json with created reminder object

### Reminders

Reminder object is
```json
{
 
      "id": 1, 
      "creation_date": "2018-01-04T21:27:55", 
      "author": <user object>, 
      "comment": "some comment",
      "task_id": 2
}
```