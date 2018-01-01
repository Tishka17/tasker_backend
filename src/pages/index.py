#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_optional, get_jwt_identity

from .blueprint import blueprint


@blueprint.route("/", methods=["GET"])
@jwt_optional
def get_users():
    print("jwt id:",get_jwt_identity())
    if get_jwt_identity():
        return flask.redirect("/users/self", 303)
    else:
        return flask.redirect("/login", 303)
