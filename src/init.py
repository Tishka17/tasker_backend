#!/usr/bin/env python
# -*- coding: utf-8 -*-

import model
import model.user
import model.authorization
import model.visibility

from werkzeug.security import generate_password_hash


def deploy(app):
    model.db.create_all(app=app)
    if not model.db.session.query(model.user.User.id).count():
        user = model.user.User(
            login="root",
            confirmed=True,
            blocked=False,
            public_visibility=model.visibility.Visibility.invisible,
            subscribers_visibility=model.visibility.Visibility.invisible,
        )
        user_auth = model.authorization.UserAuth(
            user=user,
            password_hash=generate_password_hash("password"),
        )

        model.db.session.add(user)
        model.db.session.add(user_auth)
        model.db.session.commit()
