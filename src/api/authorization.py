#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

import viewmodel.authorization

blueprint = flask.Blueprint("authorization", __name__)


@blueprint.route("/login", methods=["POST"])
def login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    return viewmodel.authorization.auth_by_login(login, password)


@blueprint.route("/vk", methods=["POST"])
def vk():
    pass
