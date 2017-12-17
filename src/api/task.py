#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required, current_identity
import datetime

import model
import model.task
import converters.task
import converters.datetime
import operations.task

blueprint = flask.Blueprint("tasks", __name__)


@blueprint.route("/", methods=["POST"])
@jwt_required()
def new_task():
    task = converters.task.from_dict(flask.request.json)
    task.owner_id = int(current_identity)
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


@blueprint.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    orig = model.task.Task.query.get(task_id)
    if not orig:
        return "Task not found", 404
    new = converters.task.from_dict(flask.request.json)
    operations.task.update(orig, new)
    model.db.session.commit()
    return flask.jsonify(data=converters.task.to_dict(orig))


@blueprint.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    orig = model.task.Task.query.get(task_id)
    if not orig:
        return "Task not found", 404
    model.db.session.delete(orig)
    model.db.session.commit()
    return flask.jsonify(data={})


@blueprint.route("/<int:task_id>/start", methods=["PUT"])
@jwt_required()
def start(task_id):
    orig = model.task.Task.query.get(task_id)
    if not orig:
        return "Task not found", 404
    if not orig.owner_id == int(current_identity):
        return "Access denied", 403
    operations.task.start(orig)
    model.db.session.commit()
    return flask.jsonify(data=converters.task.to_dict(orig))


@blueprint.route("/<int:task_id>/pause", methods=["PUT"])
@jwt_required()
def pause(task_id):
    orig = model.task.Task.query.get(task_id)
    if not orig:
        return "Task not found", 404
    if not orig.owner_id == int(current_identity):
        return "Access denied", 403
    operations.task.pause(orig)
    model.db.session.commit()
    return flask.jsonify(data=converters.task.to_dict(orig))


@blueprint.route("/<int:task_id>/finish", methods=["PUT"])
@jwt_required()
def finish(task_id):
    orig = model.task.Task.query.get(task_id)
    if not orig:
        return "Task not found", 404
    if not orig.owner_id == int(current_identity):
        return "Access denied", 403
    operations.task.finish(orig)
    model.db.session.commit()
    return flask.jsonify(data=converters.task.to_dict(orig))
