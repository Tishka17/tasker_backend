#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import converters.user
import viewmodel.user
import viewmodel.errors
from .blueprint import blueprint


@blueprint.errorhandler(viewmodel.errors.NotFoundException)
def not_found(error):
    return flask.jsonify(error=str(error)), 404


@blueprint.errorhandler(viewmodel.errors.AccessDeniedException)
def access_denied(error):
    return flask.jsonify(error=str(error)), 403


@blueprint.route("/users", methods=["GET"])
@jwt_required
def get_users():
    res = viewmodel.user.get_users()
    return flask.jsonify(data=converters.user.many_to_dict(res.items))


@blueprint.route("/users/<int:user_id>", methods=["GET"])
@blueprint.route("/users/self", methods=["GET"])
@jwt_required
def get_user(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    user = viewmodel.user.get(user_id)
    return flask.jsonify(data=converters.user.to_dict(user))


@blueprint.route("/users/<int:user_id>/tasks", methods=["GET"])
@blueprint.route("/users/self/tasks", methods=["GET"])
@jwt_required
def get_user_tasks(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    res = viewmodel.user.get_user_tasks(user_id)
    return flask.jsonify(data=converters.task.many_to_dict(res.items))
