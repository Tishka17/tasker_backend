#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db


class UserAuth(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=False)
    password_hash = db.Column(db.String(128), nullable=True)
