#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

import model.user
import render.user

blueprint = flask.Blueprint("users", __name__)


@blueprint.route("/", methods=["GET"])
def get_users(offset=0, limit=20):
    res = model.user.User.query.paginate(offset, limit, False)
    return flask.jsonify(data=render.user.many_to_dict(res.items))


@blueprint.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    res = model.user.User.query.get(user_id)
    if not res:
        return "User not found", 404
    return flask.jsonify(data=render.user.to_dict(res))
