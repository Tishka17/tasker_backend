#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import flask_jwt_extended

import use_cases.authorization
from .blueprint import blueprint


@blueprint.route("/auth/login", methods=["POST"])
def auth_login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    access_token, refresh_token = use_cases.authorization.auth_by_login(login, password)
    return flask.jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )


@blueprint.route("/auth/vk", methods=["POST"])
def auth_vk():
    code = flask.request.form["code"]
    access_token, refresh_token = use_cases.authorization.auth_by_vk(code)
    return flask.jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )


@blueprint.route("/auth/google", methods=["POST"])
def auth_google():
    code = flask.request.form["code"]
    access_token, refresh_token = use_cases.authorization.auth_by_google(code)
    return flask.jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )


@blueprint.route("/auth/refresh", methods=["POST"])
@flask_jwt_extended.jwt_refresh_token_required
def auth_refresh():
    access_token, refresh_token = use_cases.authorization.refresh(flask_jwt_extended.get_jwt_identity())
    return flask.jsonify(
        access_token=access_token,
        refresh_token=refresh_token
    )
