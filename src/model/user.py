#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
from .authorization import UserAuth


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(128), nullable=False)
    about = db.Column(db.String(1024), nullable=True)
    registration_date = db.Column(db.DateTime, default=db.func.now())
    blocked = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
