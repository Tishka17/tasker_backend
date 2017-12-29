#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jinja2
from .blueprint import blueprint

@jinja2.contextfilter
@blueprint.app_template_filter('isodate')
def jinja2_filter_isodate(app, date):
    return date.isoformat()
