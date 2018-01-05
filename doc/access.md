### Access rules

#### Task

User can **VIEW** task if:
* User is owner
* User if approved subscriber of owner and
    * Task `subscribers_visibility` is set to other than `invisible`
    * Task `subscribers_visibility` is not set and `owner.subscribers_visibility` is something else then `invisible`
* User neither owner nor approves subscriber and 
    * Task `public_visibility` is set to other than `invisible`
    * Task `public_visibility` is not set and `owner.public_visibility` is something else then `invisible`

Only owner of task can **EDIT** and **DELETE** it.


#### User

Anyone can **VIEW** user profile.
 
User can **EDIT** only his profile


#### Reminder

Only owner of task and author of reminder can **VIEW** reminder
No one can **EDIT** reminder.
Author of reminder can **DELETE** it. 