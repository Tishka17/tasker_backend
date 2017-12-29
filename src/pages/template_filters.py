#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jinja2
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
