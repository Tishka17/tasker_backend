#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import viewmodel.errors

blueprint = flask.Blueprint("pages", __name__)


@blueprint.errorhandler(viewmodel.errors.NotFoundException)
def not_found(error):
    return flask.render_template("404.html", error=str(error)), 404


@blueprint.errorhandler(viewmodel.errors.AccessDeniedException)
def access_denied(error):
    return flask.render_template("403.html", error=str(error)), 403


@blueprint.errorhandler(viewmodel.errors.InvalidCredentials)
def invalid_cred(error):
    return flask.render_template("401.html", error=str(error)), 401
