#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user
import model.external_account
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token
)

import werkzeug.security
import requests
import flask

import use_cases.errors

jwt = JWTManager()


@jwt.user_loader_callback_loader
def user_loader_callback(user_id):
    return model.user.User.query.filter_by(id=user_id).one_or_none()


def handle_auth(user):
    if user \
            and user.confirmed \
            and not user.blocked:
        return create_access_token(user.id), create_refresh_token(user.id)
    else:
        raise use_cases.errors.UserBlocked()


def refresh(user_id):
    user = model.user.User.query.filter_by(id=user_id).one_or_none()
    return handle_auth(user)


def auth_by_login(login, password):
    user = model.user.User.query.filter_by(login=login).one_or_none()
    if user \
            and user.confirmed \
            and not user.blocked \
            and user.authorization \
            and werkzeug.security.check_password_hash(user.authorization.password_hash, password):
        return handle_auth(user)
    else:
        raise use_cases.errors.InvalidCredentials()


def vk_make_redirect_url():
    return "%s/login/vk" % flask.current_app.config["BASE_URL"]


def auth_by_vk(code):
    client_id = flask.current_app.config["VK_CLIENT_ID"]
    client_secret = flask.current_app.config["VK_SECRET_KEY"]

    response = requests.get("https://oauth.vk.com/access_token?redirect_uri=%s" % vk_make_redirect_url(), params={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }).json()
    response = requests.get("https://api.vk.com/method/users.get", params={
        "access_token": response["access_token"],
        "fields": "sex,bdate,about,deactivated"
    }).json()
    if not response or not response.get("response"):
        raise use_cases.errors.InvalidCredentials()
    vk_user = response.get("response")[0]
    external_auth = model.external_account.ExternalAccount.query.filter_by(
        type="vk",
        external_id=str(vk_user["uid"])
    ).one_or_none()
    if not external_auth:
        user = model.user.User(
            name="{first_name} {last_name}".format(**vk_user).strip(),
            about=vk_user.get("about"),
            confirmed=True
        )
        external_auth = model.external_account.ExternalAccount(
            type="vk",
            external_id=str(vk_user["uid"]),
            user=user
        )
        model.db.session.add(user)
        model.db.session.add(external_auth)
        model.db.session.commit()
    else:
        user = external_auth.user
        if not user or not user.confirmed or user.blocked:
            raise use_cases.errors.InvalidCredentials()
    return handle_auth(user)


def google_make_redirect_url():
    return "%s/login/google" % flask.current_app.config["BASE_URL"]


def auth_by_google(code):
    client_id = flask.current_app.config["GOOGLE_CLIENT_ID"]
    client_secret = flask.current_app.config["GOOGLE_SECRET_KEY"]

    response = requests.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": google_make_redirect_url(),
        }
    ).json()
    google_user = requests.get("https://www.googleapis.com/plus/v1/people/me", params={
        "access_token": response["access_token"],
        "fields": "aboutMe,birthday,displayName,gender,id,image,nickname,verified"
    }).json()
    print(google_user)
    if not response:
        raise use_cases.errors.InvalidCredentials()
    external_auth = model.external_account.ExternalAccount.query.filter_by(
        type="google",
        external_id=str(google_user["id"])
    ).one_or_none()
    if not external_auth:
        user = model.user.User(
            name=google_user.get("displayName").strip(),
            confirmed=True
        )
        external_auth = model.external_account.ExternalAccount(
            type="google",
            external_id=str(google_user["id"]),
            user=user
        )
        model.db.session.add(user)
        model.db.session.add(external_auth)
        model.db.session.commit()
    else:
        user = external_auth.user
        if not user or not user.confirmed or user.blocked:
            raise use_cases.errors.InvalidCredentials()
    return handle_auth(user)
