#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required

import model.task
import render.task

blueprint = flask.Blueprint("tasks", __name__)


@blueprint.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    offset = 0
    limit = 20
    res = model.task.Task.query.paginate(offset, limit, False)
    return flask.jsonify(data=render.task.many_to_dict(res.items))


@blueprint.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_user(task_id):
    res = model.task.Task.query.get(task_id)
    if not res:
        return "User not found", 404
    return flask.jsonify(data=render.task.to_dict(res))
