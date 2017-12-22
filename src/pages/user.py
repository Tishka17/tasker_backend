#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import viewmodel.user
from .blueprint import blueprint


@blueprint.route("/users/self", methods=["GET"])
@jwt_required
def user_get():
    user = viewmodel.user.get(get_jwt_identity())
    return flask.render_template(
        "user.html",
        user=user
    )
