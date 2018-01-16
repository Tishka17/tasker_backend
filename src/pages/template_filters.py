#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jinja2
import flask
from flask_jwt_extended import get_jwt_identity
from .blueprint import blueprint


@jinja2.contextfilter
@blueprint.app_template_filter('isodate')
def jinja2_filter_isodate(_, date):
    if not date:
        return ""
    return date.isoformat()


@jinja2.contextfilter
@blueprint.app_template_filter('enum')
def jinja2_filter_visibility(_, enum):
    if not enum:
        return ""
    return enum.value


@blueprint.context_processor
def inject_current_user():
    return {"current_user_id": get_jwt_identity()}


def url_for_other_page(page):
    args = flask.request.args.copy()
    args['page'] = page
    return flask.url_for(flask.request.endpoint, **args)
