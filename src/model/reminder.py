#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db


class Reminder(db.Model):
    date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(128))
