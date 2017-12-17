#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum

from . import db
from . import visibility


@enum.unique
class Priority(enum.Enum):
    low = "low"
    middle = "middle"
    high = "high"


@enum.unique
class State(enum.Enum):
    started = "started"
    finished = "finished"
    paused = "paused"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    modification_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)
    deadline = db.Column(db.DateTime)
    title = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    priority = db.Column(db.Enum(Priority))
    state = db.Column(db.Enum(State))
    percent_progress = db.Column(db.Integer)
    public_visibility = db.Column(db.Enum(visibility.Visibility), nullable=True)
    subscribers_visibility = db.Column(db.Enum(visibility.Visibility), nullable=True)

    @db.validates("percent_progress")
    def validate_progress(self, progress):
        assert 0 <= progress <= 100
        return progress
