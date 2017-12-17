#!/usr/bin/env python
# -*- coding: utf-8 -*-

import werkzeug.security
import flask_jwt
import flask

import model.user
import render.user

jwt = flask_jwt.JWT()
blueprint = flask.Blueprint("authorization", __name__)


@blueprint.route("/login", methods=["POST"])
def login():
    login = flask.request.form["login"]
    password = flask.request.form["password"]
    user = model.user.User.query.filter_by(login=login).one_or_none()
    if user \
            and user.authorization \
            and werkzeug.security.check_password_hash(user.authorization.password_hash, password):
        return handle_auth(user)
    else:
        raise flask_jwt.JWTError('Bad Request', 'Invalid credentials')


@blueprint.route("/vk", methods=["POST"])
def vk():
    pass


def handle_auth(user):
    if user \
            and user.confirmed \
            and not user.blocked:
        access_token = jwt.jwt_encode_callback(user)
        return jwt.auth_response_callback(access_token, identity)
    else:
        raise flask_jwt.JWTError('Bad Request', 'Invalid credentials')


@jwt.identity_handler
def identity(payload):
    return str(payload["user_id"])


@jwt.jwt_payload_handler
def make_payload(idnt: model.user.User):
    res = flask_jwt._default_jwt_payload_handler(idnt)
    res.update({"user_id": idnt.id})
    return res
