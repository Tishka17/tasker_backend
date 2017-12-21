#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import viewmodel.user

blueprint = flask.Blueprint("user", __name__)


@blueprint.route("/", methods=["GET"])
@jwt_required
def get():
    user = viewmodel.user.get(get_jwt_identity())
    return flask.render_template(
        "user.html",
        login=user.login
    )
