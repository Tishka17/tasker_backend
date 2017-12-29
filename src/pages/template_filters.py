#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jinja2
from flask_jwt_extended import get_jwt_identity
from .blueprint import blueprint


@jinja2.contextfilter
@blueprint.app_template_filter('isodate')
def jinja2_filter_isodate(app, date):
    if not date:
        return ""
    return date.isoformat()


@jinja2.contextfilter
@blueprint.app_template_filter('enum')
def jinja2_filter_visibility(app, enum):
    if not enum:
        return ""
    return enum.value


@blueprint.context_processor
def inject_current_user():
    return {"current_user_id": get_jwt_identity()}
