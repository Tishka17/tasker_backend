#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import flask_jwt_extended.exceptions
import flask_wtf.csrf
import jwt.exceptions
import use_cases.errors

blueprint = flask.Blueprint("pages", __name__)


@blueprint.errorhandler(use_cases.errors.NotFoundException)
def not_found(error):
    return flask.render_template("404.html", error=str(error)), 404


@blueprint.route("/<path:path>")
def unknown_path(path):
    return flask.render_template("404.html", error="Unknown path `%s`" % path), 404


@blueprint.errorhandler(flask_jwt_extended.exceptions.CSRFError)
@blueprint.errorhandler(use_cases.errors.AccessDeniedException)
def access_denied(error):
    return flask.render_template("403.html", error=str(error)), 403


@blueprint.errorhandler(jwt.exceptions.ExpiredSignatureError)
@blueprint.errorhandler(jwt.exceptions.InvalidTokenError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.JWTDecodeError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.InvalidHeaderError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.NoAuthorizationError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.WrongTokenError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.RevokedTokenError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.FreshTokenRequired)
@blueprint.errorhandler(flask_jwt_extended.exceptions.UserLoadError)
@blueprint.errorhandler(flask_jwt_extended.exceptions.UserClaimsVerificationError)
@blueprint.errorhandler(use_cases.errors.InvalidCredentials)
def invalid_cred(error):
    return flask.render_template("401.html", error=str(error)), 401


@blueprint.errorhandler(flask_wtf.csrf.CSRFError)
def csrf_error(error):
    return flask.render_template("403.html", error=str(error)), 403
