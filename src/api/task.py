#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import converters.task
import converters.datetime
import converters.reminder
import viewmodel.task
import viewmodel.errors
from .blueprint import blueprint


@blueprint.errorhandler(viewmodel.errors.NotFoundException)
def not_found(error):
    return flask.jsonify(error=str(error)), 404


@blueprint.errorhandler(viewmodel.errors.AccessDeniedException)
def access_denied(error):
    return flask.jsonify(error=str(error)), 403


@blueprint.route("/tasks", methods=["POST"])
@jwt_required
def new_task():
    task = viewmodel.task.create(
        int(get_jwt_identity()),
        converters.task.from_dict(flask.request.json),
    )
    print(task)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/", methods=["GET"])
@jwt_required
def get_tasks():
    res = viewmodel.task.get_list()
    return flask.jsonify(data=converters.task.many_to_dict(res))


@blueprint.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required
def get_task(task_id):
    res = viewmodel.task.get(task_id)
    return flask.jsonify(data=converters.task.to_dict(res))


@blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required
def update_task(task_id):
    new = converters.task.from_dict(flask.request.json)
    task = viewmodel.task.update(int(get_jwt_identity()), task_id, new)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required
def delete_task(task_id):
    viewmodel.task.delete(int(get_jwt_identity()), task_id)
    return flask.jsonify(data={})


@blueprint.route("/tasks/<int:task_id>/start", methods=["PUT"])
@jwt_required
def start(task_id):
    task = viewmodel.task.start(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/pause", methods=["PUT"])
@jwt_required
def pause(task_id):
    task = viewmodel.task.pause(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/finish", methods=["PUT"])
@jwt_required
def finish(task_id):
    task = viewmodel.task.finish(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/remind", methods=["POST"])
@jwt_required
def remind(task_id):
    json = flask.request.json
    comment = json.get("comment") if json else None
    reminder = viewmodel.task.remind(int(get_jwt_identity()), task_id, comment)
    return flask.jsonify(data=converters.reminder.to_dict(reminder))
