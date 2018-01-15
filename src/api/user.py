#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
from flask_jwt_extended import jwt_required, get_jwt_identity

import converters.user
import converters.task
import converters.reminder
import converters.query_params
import use_cases.user
import use_cases.task
import use_cases.errors
from .blueprint import blueprint


@blueprint.route("/users", methods=["GET"])
@jwt_required
def get_users():
    res = use_cases.user.get_users(
        **converters.query_params.get_pagination_params(),
    )
    return flask.jsonify(data=converters.user.many_to_dict(res.items))


@blueprint.route("/users/<int:user_id>", methods=["GET"])
@blueprint.route("/users/self", methods=["GET"])
@jwt_required
def get_user(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    user = use_cases.user.get(user_id)
    return flask.jsonify(data=converters.user.to_dict(user))


@blueprint.route("/users/self", methods=["PUT"])
@jwt_required
def update_self():
    new = converters.user.from_dict(flask.request.json)
    user = use_cases.user.update_profile(get_jwt_identity(), new_user=new)
    return flask.jsonify(data=converters.user.to_dict(user))


@blueprint.route("/users/<int:user_id>/tasks", methods=["GET"])
@blueprint.route("/users/self/tasks", methods=["GET"])
@jwt_required
def get_user_tasks(user_id=None):
    if user_id is None:
        user_id = int(get_jwt_identity())
    res = use_cases.task.get_user_list(
        user_id,
        **converters.query_params.get_pagination_params(),
        **converters.query_params.get_task_list_params()
    )
    return flask.jsonify(data=converters.task.many_to_dict(res.items))


@blueprint.route("/users/self/reminders", methods=["GET"])
@jwt_required
def get_user_reminders():
    reminders = use_cases.user.get_reminders(
        get_jwt_identity(),
        **converters.query_params.get_pagination_params(),
    )
    return flask.jsonify(data=converters.reminder.many_to_dict(reminders.items))


@blueprint.route("/users/self/sent_reminders", methods=["GET"])
@jwt_required
def get_user_sent_reminders():
    reminders = use_cases.user.get_sent_reminders(
        get_jwt_identity(),
        **converters.query_params.get_pagination_params(),
    )
    return flask.jsonify(data=converters.reminder.many_to_dict(reminders.items))
