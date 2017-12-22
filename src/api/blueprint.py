#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import viewmodel.errors

blueprint = flask.Blueprint("api", __name__)


@blueprint.errorhandler(viewmodel.errors.NotFoundException)
def not_found(error):
    return flask.jsonify(error=str(error)), 404


@blueprint.errorhandler(viewmodel.errors.AccessDeniedException)
def access_denied(error):
    return flask.jsonify(error=str(error)), 403


@blueprint.errorhandler(viewmodel.errors.InvalidCredentials)
def invalid_creds(error):
    return flask.jsonify(error=str(error)), 401
