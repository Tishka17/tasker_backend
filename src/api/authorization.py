#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import flask_jwt_extended

import use_cases.authorization
from .blueprint import blueprint


def render_result(access_token, refresh_token, csrf_token):
    return flask.jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        csrf_token=csrf_token
    )


@blueprint.route("/auth/login", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
def auth_login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    return render_result(*use_cases.authorization.auth_by_login(login, password))


@blueprint.route("/auth/vk", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
def auth_vk():
    code = flask.request.form["code"]
    return render_result(*use_cases.authorization.auth_by_vk(code))


@blueprint.route("/auth/google", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
def auth_google():
    code = flask.request.form["code"]
    return render_result(*use_cases.authorization.auth_by_google(code))


@blueprint.route("/auth/refresh", methods=["POST"])
@use_cases.authorization.csrf_protect.exempt
@flask_jwt_extended.jwt_refresh_token_required
def auth_refresh():
    return render_result(*use_cases.authorization.refresh(flask_jwt_extended.get_jwt_identity()))
