#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.enum
import model.task
import model.reminder
from . import errors


def create(user_id: int, task: model.task.Task) -> model.task.Task:
    task.owner_id = int(user_id)
    model.db.session.add(task)
    model.db.session.commit()
    return task


def update(user_id: int, task_id: int, new: model.task.Task) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.title = new.title
    task.description = new.description
    task.deadline = new.deadline
    task.priority = new.priority
    task.subscribers_visibility = new.subscribers_visibility
    task.public_visibility = new.public_visibility

    model.db.session.commit()
    return task


def start(user_id: int, task_id: int) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.state = model.enum.State.started
    model.db.session.commit()
    return task


def pause(user_id: int, task_id: int, ) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.state = model.enum.State.paused
    model.db.session.commit()
    return task


def finish(user_id: int, task_id: int, ) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.state = model.enum.State.finished
    model.db.session.commit()
    return task


def delete(user_id: int, task_id):
    task = get_owned(user_id=user_id, task_id=task_id)

    model.db.session.delete(task)
    model.db.session.commit()


def get(task_id):
    task = model.task.Task.query.get(task_id)
    if not task:
        raise errors.NotFoundException("Task %s not found" % task_id)
    return task


def get_owned(user_id, task_id):
    task = get(task_id)
    if task.owner_id != user_id:
        raise errors.AccessDeniedException("User %s is not owner of task %s" % (user_id, task_id))
    return task


def _query_list(not_before=None, not_after=None, modified_after=None):
    query = model.task.Task.query
    if not_before:
        query = query.filter(model.task.Task.creation_date >= not_before)
    if not_after:
        query = query.filter(model.task.Task.creation_date < not_after)
    if modified_after:
        query = query.filter(model.task.Task.modification_date >= modified_after) \
            .order_by(model.task.Task.modification_date) \
            .order_by(model.task.Task.id)
    return query


def get_list(page=1, limit=20, not_before=None, not_after=None, modified_after=None):
    return _query_list(
        not_before=not_before,
        not_after=not_after,
        modified_after=modified_after
    ).paginate(page, limit, False).items


def get_user_list(user_id, page=1, limit=20, not_before=None, not_after=None, modified_after=None):
    return _query_list(
        not_before=not_before,
        not_after=not_after,
        modified_after=modified_after
    ).filter_by(owner_id=user_id).paginate(page, limit, False).items


def remind(user_id: int, task_id: int, comment: str) -> model.reminder.Reminder:
    task = get(task_id)
    reminder = model.reminder.Reminder(
        task=task,
        author_id=user_id,
        comment=comment
    )
    model.db.session.add(reminder)
    model.db.session.commit()
    return reminder


def get_reminders(user_id, task_id, page=1, limit=20):
    task = get(task_id)
    if task.owner_id != user_id:
        raise errors.AccessDeniedException("User %s is not owner of task %s" % (user_id, task_id))
    return model.reminder.Reminder.query.filter_by(task_id=task_id).paginate(page, limit, False)
