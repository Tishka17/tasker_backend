#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import backref

from . import db
from . import enum
from .user import User


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    modification_date = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship(User, backref=backref('tasks', cascade="all,delete"))
    deadline = db.Column(db.DateTime)
    title = db.Column(db.String(128))
    description = db.Column(db.String(1024))
    priority = db.Column(enum.SqlPriority)
    state = db.Column(enum.SqlState)
    percent_progress = db.Column(db.Integer)
    public_visibility = db.Column(enum.SqlVisibility, nullable=True)
    subscribers_visibility = db.Column(enum.SqlVisibility, nullable=True)

    @db.validates("percent_progress")
    def validate_progress(self, progress):
        assert 0 <= progress <= 100
        return progress
