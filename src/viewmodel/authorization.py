#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user
import model.external_account
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity
)

import werkzeug.security
import requests

jwt = JWTManager()


def handle_auth(user):
    if user \
            and user.confirmed \
            and not user.blocked:
        return create_access_token(user.id)
    else:
        raise None #flask_jwt.JWTError('Bad Request', 'Invalid credentials')

#
# @jwt.identity_handler
# def identity(payload):
#     return payload["user_id"]
#
#
# @jwt.jwt_payload_handler
# def make_payload(idnt: model.user.User):
#     res = flask_jwt._default_jwt_payload_handler(idnt)
#     res.update({"user_id": idnt.id})
#     return res


def auth_by_login(login, password):
    user = model.user.User.query.filter_by(login=login).one_or_none()
    if user \
            and user.confirmed \
            and not user.blocked \
            and user.authorization \
            and werkzeug.security.check_password_hash(user.authorization.password_hash, password):
        return handle_auth(user)
    else:
        raise None #flask_jwt.JWTError('Bad Request', 'Invalid credentials')


def make_redirect_url():
    return "http://127.0.0.1"


def auth_by_vk(code):
    client_id, client_secret = None, None  # TODO: from config
    responce = requests.get("https://oauth.vk.com/access_token?redirect_uri=%s" % make_redirect_url(), params={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }).json()
    responce = requests.get("https://api.vk.com/method/users.get", params={
        "access_token": responce["access_token"],
        "fields": "sex,bdate,about,deactivated"
    }).json()

    external_auth = model.external_account.ExternalAccount.query.get(type="vk", external_id=responce["id"])
    if not external_auth:
        user = model.user.User(
            name="{first_name} {last_name}".format(responce).strip(),
            about=responce.get("about"),
            confirmed=True
        )
        external_auth = model.external_account.ExternalAccount(
            type="vk",
            external_id=responce["id"],
            user=user
        )
        model.db.session.add(user)
        model.db.session.add(external_auth)
        model.db.session.commit()
    else:
        user = external_auth.user
        if not user or not user.confirmed or user.blocked:
            raise flask_jwt.JWTError('Bad Request', 'Invalid credentials')
    return handle_auth(user)
