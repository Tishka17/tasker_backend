#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

import use_cases.authorization
from .blueprint import blueprint


@blueprint.route("/auth/login", methods=["POST"])
def auth_login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    access_token = use_cases.authorization.auth_by_login(login, password)
    return flask.jsonify(access_token=access_token), 200


@blueprint.route("/auth/vk", methods=["POST"])
def auth_vk():
    code = flask.request.form["code"]
    access_token = use_cases.authorization.auth_by_vk(code)
    return flask.jsonify(access_token=access_token), 200
