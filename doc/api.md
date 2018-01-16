## API Endpoints

### Base info

Base url for all requests is `/api/v1`
To get access token see authorization endpoint.

 
To use any api method (except authorization) you should send `Authorization` with Bearer type and access token. E.g.

```
Authorization: Bearer your_access_token
```

All responses consist of json with `error` or `data` field.
If there is no errors, requested object (or list of objects) is returned in `data` field. 
If list was requested, result will also containt Pagination object.


### Authorization

The response of authotization request is object. Currently there is only `acess_token` available.
E.g.:
```json
{
  "access_token": "your access token",
  "refresh_token": "your refresh token"
}
```

#### login+password `/auth/login`

* **Method**: POST 
* **In** (x-www-form-urlencoded):
    * login - login as in set in user profile
    * password - password and was set by user
* **Out** (json): authorization result object

#### Refresh `/auth/refresh`

If your access_token is expired, you can get new one.
Set authorization header with you `refresh_token`. The response will contain new access and refresh tokens

```
Authorization: Bearer your_refresh_token
```


#### vk.com `/auth/vk`
To get code from vk you should open a page with url: 
```url
https://oauth.vk.com/authorize?client_id={{client_id}}&response_type=code&redirect_uri={{redirect_url}}
```

And then wait for opening redirect_uri with code in url params.

Client id and redirect url should be requested from current site author.

* **Method**: POST 
* **In** (x-www-form-urlencoded): code, returned by vk oauth api
* **Out** (json): authorization result object

#### google.com `/auth/google`
Client id and redirect url should be requested from current site author.

* **Method**: POST 
* **In** (x-www-form-urlencoded): code, returned by google oauth api
* **Out** (json): authorization result object


### Types

* Datetime is provided in iso format
* Visibility is enum with values: `full`, `title_only`, `presence_only`, `invisible`
* Priority is enum with values: `low`, `medium`, `high`

### Pagination

All methods, returning list support HTTP GET params such as
* `limit` - number of items per page
* `page` - requested number of page

The response will contain pagination object, which has such fields:
* `has_next` - true if next page is available
* `has_prev` - true if next page is available
* `pages` - total number of pages
* `page` - current page
* `per_page` - items count per page 
* `prev_num` - number of previous page
* `next_num` - number of next page


### User

In all user methods you can use `self` insted of `user_id` if you want to user current logged in user id.

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

#### List of users `/users`

* **Method**: GET 
* **In** (url params): page, limit
* **Out**: array of user objects

#### User info `/users/user_id`
* **Method**: GET
* **Out**: user object

#### Update user info `/users/self`
* **Method**: PUT
* **In** (json): user object
* **Out**: updated user object

Only these fields can be updated:
* login
* name
* about
* subscribers_visibility
* public_visibility

#### Get user tasks `/users/user_id/tasks`
* **Method**: GET
* **In** (url params): same as in `/tasks/` (list of all tasks)
* **Out**: array of user tasks (can be empty if user has now tasks)

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

#### Create new task `/tasks`
 **Method**: POST
* **In** (json):  task object
* **Out**: created task object

Only these fields are should be provided:
* title
* description
* deadline (datetime, see types)
* priority (enum, see types)
* public_visibility
* subscribers_visibility

#### Get List of tasks `/tasks/`
* **Method**: GET
* **In** (url params): 
    * `page` (optional) - number of page 
    * `limit` (optional) - limit records per page. Default, 20 
    * `deadline_before` (optional) - datetime in isoformat. 
        Filter tasks with deadline before date provided (excluding). Not checked by default
    * `deadline_after` (optional) - datetime in isoformat.
        Filter tasks with deadline after date provided (including). Not checked by default
    * `modified_after` (optional) - datetime in isoformat.
        Filter tasks changed after date provided (including). Not checked by default
    * `no_deadline` (optional) - any non empty value.
        If present filter only tasks with no deadline set. Do not set together with other deadline filters.
    * `include_finished` (optional) - any non empty value. 
        Include tasks with state `finished`. In not present, finished tasks are omitted
* **Out**: array of task objects

Tasks are sorted by modifiaction_date if `modified_after` was set. Otherwie they are sorted by id.

#### Get task by id `/tasks/task_id`
* **Method**: GET
* **Out**: task object

#### Update task by id `/tasks/task_id`
* **Method**: PUT
* **In**: json with task object
* **Out**: json with updated task object

Only some fields can be updated. See creating new task

#### Delete task by id `/tasks/task_id`
* **Method**: DELETE
* **Out**: empty object

#### Update task state
`**PUT** /tasks/task_id/start"`
* Out: json with updated task object

`**PUT** /tasks/task_id/pause"`
* Out: json with updated task object

`**PUT** /tasks/task_id/finish"`
* Out: json with updated task object


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

#### Create task reminder by task id `/tasks/task_id/remind`
* **Method**: POST
* **In** (json): reminder object
* **Out**: created reminder object

#### Get reminders by task id `/tasks/task_id/reminders`
* **Method**: GET
* **In** (url params): page, limit
* **Out** (json): array of reminder objects

#### Get received reminders`/users/self/reminders`
* **Method**: GET
* **In** (url params): page, limit
* **Out** (json): array of reminder objects

#### Get sent reminders`/users/self/sent_reminders`
* **Method**: GET
* **In** (url params): page, limit
* **Out** (json): array of reminder objects
