#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import model.visibility
import converters.task
import converters.datetime
import converters.reminder
import use_cases.task
from .blueprint import blueprint


@blueprint.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required
def get_task(task_id):
    print("!!!!!")
    res = use_cases.task.get(task_id)
    return flask.render_template(
        "task.html",
        task=res
    )


@blueprint.route("/tasks/<int:task_id>/edit", methods=["GET"])
@jwt_required
def get_edit_task(task_id):
    res = use_cases.task.get(task_id)
    return flask.render_template(
        "task_edit.html",
        task=res,
        visibilities=model.visibility.Visibility
    )


@blueprint.route("/tasks/<int:task_id>", methods=["POST"])
@jwt_required
def update_task(task_id):
    use_cases.task.update(get_jwt_identity(), task_id, converters.task.from_dict(flask.request.form))
    return flask.redirect(location=flask.url_for("pages.get_task", task_id=task_id), code=302)


@blueprint.route("/tasks/", methods=["POST"])
@jwt_required
def create_task():
    task = use_cases.task.create(get_jwt_identity(), converters.task.from_dict(flask.request.form))
    return flask.redirect(location=flask.url_for("pages.get_task", task_id=task.id), code=302)
