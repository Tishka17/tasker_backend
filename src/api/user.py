#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import converters.user
import use_cases.user
import use_cases.errors
from .blueprint import blueprint


@blueprint.route("/users", methods=["GET"])
@jwt_required
def get_users():
    res = use_cases.user.get_users()
    return flask.jsonify(data=converters.user.many_to_dict(res.items))


@blueprint.route("/users/<int:user_id>", methods=["GET"])
@blueprint.route("/users/self", methods=["GET"])
@jwt_required
def get_user(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    user = use_cases.user.get(user_id)
    return flask.jsonify(data=converters.user.to_dict(user))


@blueprint.route("/users/self", methods=["PUT"])
@jwt_required
def update_self():
    new = converters.user.from_dict(flask.request.json)
    user = use_cases.user.update_profile(get_jwt_identity(), new_user=new)
    return flask.jsonify(data=converters.user.to_dict(user))


@blueprint.route("/users/<int:user_id>/tasks", methods=["GET"])
@blueprint.route("/users/self/tasks", methods=["GET"])
@jwt_required
def get_user_tasks(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    res = use_cases.user.get_user_tasks(user_id)
    return flask.jsonify(data=converters.task.many_to_dict(res.items))
