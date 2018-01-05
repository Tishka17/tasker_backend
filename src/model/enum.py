#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum

from . import db


@enum.unique
class Visibility(enum.Enum):
    full = "full"
    title_only = "title_only"
    presence_only = "presence_only"
    invisible = "invisible"


@enum.unique
class Priority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


@enum.unique
class State(enum.Enum):
    started = "started"
    finished = "finished"
    paused = "paused"


SqlVisibility = db.Enum(Visibility)
SqlPriority = db.Enum(Priority)
SqlState = db.Enum(State)
