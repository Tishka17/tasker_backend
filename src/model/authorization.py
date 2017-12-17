#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy.orm import backref

from . import db
from .user import User


class UserAuth(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, autoincrement=False, nullable=False)
    user = db.relationship(User, backref=backref("authorization", cascade="all,delete"))
    password_hash = db.Column(db.String(128), nullable=True)
