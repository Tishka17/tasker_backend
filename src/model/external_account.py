#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db


class ExternalAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(128))
    external_id = db.Column(db.String(256))
    __table_args__ = (
        db.UniqueConstraint("type", "external_id", name="uix_external_account"),
    )
