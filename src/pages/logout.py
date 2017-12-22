#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import flask
from flask_jwt_extended import unset_jwt_cookies, jwt_required

import viewmodel.authorization

blueprint = flask.Blueprint("logout", __name__)


@blueprint.route("/", methods=["POST"])
@jwt_required
def post():
    resp = flask.redirect("/login", code=301)
    unset_jwt_cookies(resp)
    return resp
