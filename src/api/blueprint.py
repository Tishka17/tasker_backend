#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import use_cases.errors

blueprint = flask.Blueprint("api", __name__)


@blueprint.errorhandler(use_cases.errors.NotFoundException)
def not_found(error):
    return flask.jsonify(error=str(error)), 404


@blueprint.errorhandler(use_cases.errors.AccessDeniedException)
def access_denied(error):
    return flask.jsonify(error=str(error)), 403


@blueprint.errorhandler(use_cases.errors.InvalidCredentials)
def invalid_credentials(error):
    return flask.jsonify(error=str(error)), 401


@blueprint.errorhandler(use_cases.errors.UserBlocked)
def invalid_creds(error):
    return flask.jsonify(error=str(error)), 401
