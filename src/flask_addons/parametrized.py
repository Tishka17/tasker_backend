#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import flask
from typing import List, Dict


def _get_args_dict(data: Dict, params_desc: List[str], defaults: Dict):
    args = {}
    for param_desc in params_desc:
        if defaults and param_desc in defaults:
            args[param_desc] = data.get(param_desc, defaults[param_desc])
        else:
            args[param_desc] = data[param_desc]
    return args


class Parametrized(object):
    params = None
    defaults = None

    def __init__(self, *params, defaults=None) -> None:
        super().__init__()
        self.params = params
        self.defaults = defaults

    def __call__(self, func, ):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs, **_get_args_dict(flask.request.args, self.params, self.defaults))
        return wrapped
