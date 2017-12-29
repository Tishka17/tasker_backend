#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

    task.state = model.task.State.started
    model.db.session.commit()
    return task


def pause(user_id: int, task_id: int, ) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.state = model.task.State.paused
    model.db.session.commit()
    return task


def finish(user_id: int, task_id: int, ) -> model.task.Task:
    task = get_owned(user_id=user_id, task_id=task_id)

    task.state = model.task.State.finished
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


def get_list(offset=0, limit=20):
    return model.task.Task.query.paginate(offset, limit, False).items


def get_user_list(user_id, offset=0, limit=20):
    return model.task.Task.query.filter_by(owner_id=user_id).paginate(offset, limit, False).items


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
