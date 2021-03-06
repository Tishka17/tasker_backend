#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import converters.task
import converters.datetime
import converters.reminder
import converters.pagination
import converters.query_params
import use_cases.task
from .blueprint import blueprint


@blueprint.route("/tasks", methods=["POST"])
@jwt_required
def new_task():
    task = use_cases.task.create(
        int(get_jwt_identity()),
        converters.task.from_dict(flask.request.json),
    )
    print(task)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/", methods=["GET"])
@jwt_required
def get_tasks():
    tasks = use_cases.task.get_list(
        **converters.query_params.get_pagination_params(),
        **converters.query_params.get_task_list_params(),
    )
    return flask.jsonify(
        data=converters.task.many_to_dict(tasks.items),
        pagination=converters.pagination.to_dict(tasks)
    )


@blueprint.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required
def get_task(task_id):
    res = use_cases.task.get(task_id)
    return flask.jsonify(data=converters.task.to_dict(res))


@blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required
def update_task(task_id):
    new = converters.task.from_dict(flask.request.json)
    task = use_cases.task.update(int(get_jwt_identity()), task_id, new)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required
def delete_task(task_id):
    use_cases.task.delete(int(get_jwt_identity()), task_id)
    return flask.jsonify(data={})


@blueprint.route("/tasks/<int:task_id>/start", methods=["PUT"])
@jwt_required
def start(task_id):
    task = use_cases.task.start(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/pause", methods=["PUT"])
@jwt_required
def pause(task_id):
    task = use_cases.task.pause(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/finish", methods=["PUT"])
@jwt_required
def finish(task_id):
    task = use_cases.task.finish(int(get_jwt_identity()), task_id)
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/tasks/<int:task_id>/remind", methods=["POST"])
@jwt_required
def remind(task_id):
    json = flask.request.json
    comment = json.get("comment") if json else None
    reminder = use_cases.task.remind(int(get_jwt_identity()), task_id, comment)
    return flask.jsonify(data=converters.reminder.to_dict(reminder))


@blueprint.route("/tasks/<int:task_id>/reminders", methods=["GET"])
@jwt_required
def get_task_reminders(task_id):
    reminders = use_cases.task.get_reminders(
        get_jwt_identity(),
        task_id,
        **converters.query_params.get_pagination_params(),
    )
    return flask.jsonify(
        data=converters.reminder.many_to_dict(reminders.items),
        pagination=converters.pagination.to_dict(reminders)
    )
