#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required, current_identity
import datetime

import model
import model.task
import converters.task
import converters.datetime

blueprint = flask.Blueprint("tasks", __name__)


@blueprint.route("/", methods=["POST"])
@jwt_required()
def new_task():
    data = flask.request.json
    task = model.task.Task(
        title=data.get("title"),
        description=data.get("description"),
        deadline=converters.datetime.from_str(data.get("deadline")),
        priority=data.get("priority"),
        owner_id=int(current_identity),
        public_visibility=data.get("public_visibility"),
        subscribers_visibility=data.get("subscribers_visibility")
    )
    model.db.session.add(task)
    model.db.session.commit()
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    offset = 0
    limit = 20
    res = model.task.Task.query.paginate(offset, limit, False)
    return flask.jsonify(data=converters.task.many_to_dict(res.items))


@blueprint.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    res = model.task.Task.query.get(task_id)
    if not res:
        return "Task not found", 404
    return flask.jsonify(data=converters.task.to_dict(res))
