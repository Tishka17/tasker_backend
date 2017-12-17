#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt import jwt_required, current_identity

import converters.task
import converters.datetime
import viewmodel.task
import viewmodel.errors

blueprint = flask.Blueprint("tasks", __name__)


@blueprint.route("/", methods=["POST"])
@jwt_required()
def new_task():
    task = viewmodel.task.create(
        int(current_identity),
        converters.task.from_dict(flask.request.json),
    )
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    res = viewmodel.task.get_list()
    return flask.jsonify(data=converters.task.many_to_dict(res))


@blueprint.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    try:
        res = viewmodel.task.get(task_id)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    return flask.jsonify(data=converters.task.to_dict(res))


@blueprint.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    try:
        new = converters.task.from_dict(flask.request.json)
        task = viewmodel.task.update(int(current_identity), task_id, new)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    except viewmodel.errors.AccessDeniedException:
        return "Access denied", 403
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    try:
        viewmodel.task.delete(int(current_identity), task_id)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    except viewmodel.errors.AccessDeniedException:
        return "Access denied", 403
    return flask.jsonify(data={})


@blueprint.route("/<int:task_id>/start", methods=["PUT"])
@jwt_required()
def start(task_id):
    try:
        task = viewmodel.task.start(int(current_identity), task_id)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    except viewmodel.errors.AccessDeniedException:
        return "Access denied", 403
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/<int:task_id>/pause", methods=["PUT"])
@jwt_required()
def pause(task_id):
    try:
        task = viewmodel.task.pause(int(current_identity), task_id)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    except viewmodel.errors.AccessDeniedException:
        return "Access denied", 403
    return flask.jsonify(data=converters.task.to_dict(task))


@blueprint.route("/<int:task_id>/finish", methods=["PUT"])
@jwt_required()
def finish(task_id):
    try:
        task = viewmodel.task.finish(int(current_identity), task_id)
    except viewmodel.errors.NotFoundException:
        return "Task not found", 404
    except viewmodel.errors.AccessDeniedException:
        return "Access denied", 403
    return flask.jsonify(data=converters.task.to_dict(task))
