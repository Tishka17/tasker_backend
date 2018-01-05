#!/usr/bin/env python
# -*- coding: utf-8 -*-
import typing

import model.reminder
from . import user
from . import task


def to_dict(reminder: model.reminder.Reminder) -> dict:
    return {
        "id": reminder.id,
        "creation_date": reminder.creation_date,
        "author": user.to_dict(reminder.author),
        "comment": reminder.comment,
        "task_id": reminder.task_id,
        "task": task.to_dict(reminder.task)
    }


def many_to_dict(reminders: typing.Iterable[model.reminder.Reminder]) -> typing.Generator[dict, None, None]:
    return (to_dict(reminder) for reminder in reminders)
