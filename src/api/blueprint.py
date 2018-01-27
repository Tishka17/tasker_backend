#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask
import jwt.exceptions
import flask_jwt_extended.exceptions
import flask_wtf.csrf

import use_cases.errors

blueprint = flask.Blueprint("api", __name__)


@blueprint.errorhandler(use_cases.errors.NotFoundException)
def not_found(error):
    return flask.jsonify(error=str(error)), 404


@blueprint.route("/<path:path>")
def unknown_path(path):
    return flask.jsonify(error="Object for path `%s` not found" % path), 404


@blueprint.errorhandler(flask_jwt_extended.exceptions.CSRFError)
@blueprint.errorhandler(use_cases.errors.AccessDeniedException)
def access_denied(error):
    return flask.jsonify(error=str(error)), 403


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
def invalid_credentials(error):
    return flask.jsonify(error=str(error)), 401


@blueprint.errorhandler(use_cases.errors.UserBlocked)
def user_blocked(error):
    return flask.jsonify(error=str(error)), 401


@blueprint.errorhandler(flask_wtf.csrf.CSRFError)
def csrf_error(error):
    return flask.jsonify(error=str(error.description)), 403
