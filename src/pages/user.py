#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import use_cases.user
import converters.user
import model.user
import model.visibility
from .blueprint import blueprint


@blueprint.route("/users/self", methods=["GET"])
@jwt_required
def user_get_self():
    user = use_cases.user.get(get_jwt_identity())
    return flask.render_template(
        "user.html",
        user=user
    )


@blueprint.route("/users/<int:user_id>", methods=["GET"])
@jwt_required
def user_get(user_id):
    user = use_cases.user.get(user_id)
    return flask.render_template(
        "user.html",
        user=user
    )


@blueprint.route("/users/self/edit", methods=["GET"])
@jwt_required
def self_edit_get():
    user = use_cases.user.get(get_jwt_identity())
    return flask.render_template(
        "profile_edit.html",
        user=user,
        visibilities=model.visibility.Visibility
    )


@blueprint.route("/users/self/edit", methods=["POST"])
@jwt_required
def self_edit_post():
    use_cases.user.update_profile(
        user_id=get_jwt_identity(),
        new_user=converters.user.from_dict(flask.request.form)
    )
    return flask.redirect(location=flask.url_for("pages.self_edit_post"), code=303)
