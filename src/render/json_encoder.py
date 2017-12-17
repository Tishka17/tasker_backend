#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.json import JSONEncoder
from werkzeug.local import LocalProxy
import enum
import datetime


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, LocalProxy):
                return self.default(obj._get_current_object())
            elif isinstance(obj, enum.Enum):
                return obj.value
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
