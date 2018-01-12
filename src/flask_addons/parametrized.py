#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import flask


class Parametrized(object):
    type = None
    param = None
    default = None
    required = None

    def __init__(self, param, type=str, required=True, default=None) -> None:
        super().__init__()
        self.required = required
        self.default = default
        self.type = type
        self.param = param

    def __call__(self, func, ):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            data = flask.request.args
            if self.required:
                value = self.type(data[self.param])
            else:
                value = data.get(self.param, self.default)
                if value is not None:
                    value = self.type(value)
            return func(*args, **kwargs, **{self.param: value})

        return wrapped
