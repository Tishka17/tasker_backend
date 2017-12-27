#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user

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


def update_profile(user_id, login, name, public_visibility, subscribers_visibility):
    user = get(user_id)  # type: model.user.User
    user.login = login or user.login
    user.name = name or user.name
    user.public_visibility = public_visibility or user.public_visibility
    user.subscribers_visibility = subscribers_visibility or user.subscribers_visibility
    model.db.session.add(user)
    model.db.session.commit()
