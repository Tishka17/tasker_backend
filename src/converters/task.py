#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.task
from . import user

import typing


def to_dict(task: model.task.Task) -> dict:
    return {
        "id": task.id,
        "creation_date": task.creation_date,
        "modification_date": task.modification_date,
        "owner": user.to_dict(task.owner),
        "deadline": task.deadline,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "percent_progress": task.percent_progress,
        "public_visibility": task.public_visibility,
        "subscribers_visibility": task.subscribers_visibility,
    }


def many_to_dict(tasks: typing.Iterable[model.task.Task]) -> typing.Generator[dict, None, None]:
    return (to_dict(tasks) for tasks in tasks)
