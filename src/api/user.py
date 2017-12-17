#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask import jsonify

from data import user

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=["GET"])
def get_users(offset=0, limit=20):
    res = user.User.query.offset(offset).limit(limit).all()
    return jsonify(data=res)


@user_blueprint.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    res = user.User.query.get(user_id)
    if not res:
        return "User not found", 404
    return jsonify(data=res)
