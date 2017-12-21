#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import flask

import viewmodel.authorization

blueprint = flask.Blueprint("login", __name__)


@blueprint.route("/", methods=["POST"])
def post():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    logging.debug("login POST %s %s", login, password)
    return viewmodel.authorization.auth_by_login(login, password)


@blueprint.route("/", methods=["GET"])
def get():
    return flask.render_template(
        "login.html",
        login="",
        password=""
    )
