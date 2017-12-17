#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db


class Subscription(db.Model):
    __table_args__ = (
        db.UniqueConstraint("type", "external_id", name="uix_subscription"),
    )

    from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)
