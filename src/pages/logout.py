#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import unset_jwt_cookies, jwt_optional

from .blueprint import blueprint
import use_cases.authorization


@blueprint.route("/logout", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
@jwt_optional
def logout_post():
    resp = flask.redirect("/login", code=303)
    unset_jwt_cookies(resp)
    return resp
