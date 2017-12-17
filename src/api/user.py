#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required, current_identity

import model.user
import render.user

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/", methods=["GET"])
@jwt_required()
def get_users(offset=0, limit=20):
    res = model.user.User.query.paginate(offset, limit, False)
    return flask.jsonify(data=render.user.many_to_dict(res.items))


@blueprint.route("/<int:user_id>", methods=["GET"])
@blueprint.route("/self", methods=["GET"])
@jwt_required()
def get_user(user_id=None):
    if user_id is None:
        user_id = current_identity
    print("user id =", user_id)
    res = model.user.User.query.get(user_id)
    print(res)
    if not res:
        return "User not found", 404
    return flask.jsonify(data=render.user.to_dict(res))

