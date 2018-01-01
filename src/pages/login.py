#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import flask
from flask_jwt_extended import set_access_cookies

import use_cases.authorization
from .blueprint import blueprint


@blueprint.route("/login", methods=["POST"])
def login_post():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    logging.debug("login POST %s %s", login, password)
    access_token = use_cases.authorization.auth_by_login(login, password)
    resp = flask.redirect("/users/self", code=303)
    set_access_cookies(resp, access_token)
    return resp


@blueprint.route("/login", methods=["GET"])
def login_get():
    return flask.render_template(
        "login.html",
        login="",
        password="",
        client_id=flask.current_app.config['VK_CLIENT_ID']
    )


@blueprint.route("/login/vk", methods=["GET"])
def login_vk():
    code = flask.request.args.get("code")
    access_token = use_cases.authorization.auth_by_vk(code)
    resp = flask.redirect("/users/self", code=303)
    set_access_cookies(resp, access_token)
    return resp
