#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.task
import model.enum
from . import enum
from . import user
from . import datetime

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
        "state": task.state,
        "percent_progress": task.percent_progress,
        "public_visibility": enum.to_str(task.public_visibility),
        "subscribers_visibility": enum.to_str(task.subscribers_visibility),
    }


def from_dict(data):
    return model.task.Task(
        title=data.get("title"),
        description=data.get("description"),
        deadline=datetime.from_str(data.get("deadline")),
        priority=data.get("priority"),
        public_visibility=enum.from_str(model.enum.Visibility, data.get("public_visibility")),
        subscribers_visibility=enum.from_str(model.enum.Visibility, data.get("subscribers_visibility"))
    )


def many_to_dict(tasks: typing.Iterable[model.task.Task]) -> typing.Generator[dict, None, None]:
    return (to_dict(task) for task in tasks)
