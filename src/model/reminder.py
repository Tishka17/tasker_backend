#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db


class Reminder(db.Model):
    date = db.Column(db.DateTime, default=db.func.now())
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
