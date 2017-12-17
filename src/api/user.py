#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required, current_identity

import model.user
import converters.user

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/", methods=["GET"])
@jwt_required()
def get_users(offset=0, limit=20):
    res = model.user.User.query.paginate(offset, limit, False)
    return flask.jsonify(data=converters.user.many_to_dict(res.items))


@blueprint.route("/<int:user_id>", methods=["GET"])
@blueprint.route("/self", methods=["GET"])
@jwt_required()
def get_user(user_id=None):
    if user_id is None:
        user_id = int(current_identity)
    print("user", type(user_id), user_id)
    res = model.user.User.query.get(user_id)
    print(res)
    if not res:
        return "User not found", 404
    return flask.jsonify(data=converters.user.to_dict(res))


@blueprint.route("/<int:user_id>/tasks", methods=["GET"])
@blueprint.route("/self/tasks", methods=["GET"])
@jwt_required()
def get_user_tasks(user_id=None):
    offset = 0
    limit = 20
    if user_id is None:
        user_id = int(current_identity)
    res = model.task.Task.query.filter_by(owner_id=user_id).paginate(offset, limit, False)
    return flask.jsonify(data=converters.task.many_to_dict(res.items))
