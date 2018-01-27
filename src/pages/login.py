#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import flask
from flask_jwt_extended import set_access_cookies

import use_cases.authorization
from .blueprint import blueprint


@blueprint.route("/login", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
def login_post():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    logging.debug("login POST %s %s", login, password)
    access_token, refresh_token, _ = use_cases.authorization.auth_by_login(login, password)
    resp = flask.redirect("/users/self", code=303)
    set_access_cookies(resp, access_token)
    return resp


@blueprint.route("/login", methods=["GET"])
def login_get():
    return flask.render_template(
        "login.html",
        login="",
        password="",
        vk_client_id=flask.current_app.config['VK_CLIENT_ID'],
        vk_redirect_url=use_cases.authorization.vk_make_redirect_url(),
        google_client_id=flask.current_app.config['GOOGLE_CLIENT_ID'],
        google_redirect_url=use_cases.authorization.google_make_redirect_url(),
    )


@blueprint.route("/login/vk", methods=["GET"])
def login_vk():
    code = flask.request.args["code"]
    access_token, refresh_token, _ = use_cases.authorization.auth_by_vk(code)
    resp = flask.redirect("/users/self", code=303)
    set_access_cookies(resp, access_token)
    return resp


@blueprint.route("/login/google", methods=["GET"])
def login_google():
    code = flask.request.args["code"]
    access_token, refresh_token, _ = use_cases.authorization.auth_by_google(code)
    resp = flask.redirect("/users/self", code=303)
    set_access_cookies(resp, access_token)
    return resp
