#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import backref

from .user import User
from .task import Task
from . import db


class Reminder(db.Model):
    date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship(Task, backref=backref("reminders", cascade="all,delete"))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship(User, backref=backref("sent_reminders", cascade="all,delete"))
    comment = db.Column(db.String(128))
