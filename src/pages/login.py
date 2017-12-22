#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import flask
from flask_jwt_extended import set_access_cookies

import viewmodel.authorization

blueprint = flask.Blueprint("login", __name__)


@blueprint.route("/", methods=["POST"])
def post():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    logging.debug("login POST %s %s", login, password)
    access_token = viewmodel.authorization.auth_by_login(login, password)
    resp = flask.redirect("/user", code=301)
    set_access_cookies(resp, access_token)
    return resp


@blueprint.route("/", methods=["GET"])
def get():
    return flask.render_template(
        "login.html",
        login="",
        password="",
        client_id=flask.current_app.config['VK_CLIENT_ID']
    )


@blueprint.route("/vk", methods=["GET"])
def vk():
    code = flask.request.args.get("code")
    access_token = viewmodel.authorization.auth_by_vk(code)
    resp = flask.redirect("/user", code=301)
    set_access_cookies(resp, access_token)
    return resp
