#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify

import model.user
import render.user

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["GET"])
def get_users(offset=0, limit=20):
    res = model.user.User.query.offset(offset).limit(limit).all()
    return jsonify(data=render.user.many_to_dict(res))


@user_blueprint.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    res = model.user.User.query.get(user_id)
    if not res:
        return "User not found", 404
    return jsonify(data=render.user.to_dict(res))
