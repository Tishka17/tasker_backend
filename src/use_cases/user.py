#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user
import model.enum
import model.task
import model.reminder

from . import errors


def get_users(offset=0, limit=20):
    return model.user.User.query.paginate(offset, limit, False)


def get(user_id):
    user = model.user.User.query.get(user_id)
    if not user:
        raise errors.NotFoundException("User %s not found" % user_id)
    return user


def get_user_tasks(user_id, offset=0, limit=20):
    return model.task.Task.query.filter_by(owner_id=user_id).paginate(offset, limit, False)


def update_profile(user_id, new_user):
    user = get(user_id)  # type: model.user.User
    user.login = new_user.login or user.login
    user.name = new_user.name or user.name
    user.public_visibility = new_user.public_visibility or user.public_visibility
    user.subscribers_visibility = new_user.subscribers_visibility or user.subscribers_visibility
    model.db.session.add(user)
    model.db.session.commit()
    return user


def get_reminders(user_id, offset=0, limit=20):
    query = model.reminder.Reminder.query.join(model.task.Task, model.task.Task.owner_id == user_id)
    return query.paginate(offset, limit, False)


def get_sent_reminders(user_id, offset=0, limit=20):
    return model.reminder.Reminder.query.filter_by(author_id=user_id).paginate(offset, limit, False)
