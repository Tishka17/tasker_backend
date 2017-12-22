#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import flask
from flask_jwt_extended import unset_jwt_cookies, jwt_required

from .blueprint import blueprint


@blueprint.route("/logout", methods=["POST"])
@jwt_required
def logout_post():
    resp = flask.redirect("/login", code=301)
    unset_jwt_cookies(resp)
    return resp
