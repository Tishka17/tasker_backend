#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db


class ExternalAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="externals_accounts")
    type = db.Column(db.String(128), nullable=False)
    external_id = db.Column(db.String(256), nullable=False)
    __table_args__ = (
        db.UniqueConstraint("type", "external_id", name="uix_external_account"),
    )
