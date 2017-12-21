#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

import viewmodel.authorization

blueprint = flask.Blueprint("authorization", __name__)


@blueprint.route("/login", methods=["POST"])
def login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    access_token = viewmodel.authorization.auth_by_login(login, password)
    return flask.jsonify(access_token=access_token), 200


@blueprint.route("/vk", methods=["POST"])
def vk():
    code = flask.request.form["code"]
    access_token = viewmodel.authorization.auth_by_vk(code)
    return flask.jsonify(access_token=access_token), 200
