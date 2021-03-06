#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
from . import enum


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = db.Column(db.String(128), nullable=True, unique=True)
    name = db.Column(db.String(128), nullable=True)
    about = db.Column(db.String(1024), nullable=True)
    registration_date = db.Column(db.DateTime, default=db.func.now())
    blocked = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)
    public_visibility = db.Column(enum.SqlVisibility, nullable=False, default=enum.Visibility.full)
    subscribers_visibility = db.Column(enum.SqlVisibility, nullable=False,
                                       default=enum.Visibility.full)
