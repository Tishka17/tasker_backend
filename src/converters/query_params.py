#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask


def get_pagination_params():
    return {
        "page": int(flask.request.args.get("page", 1)),
        "limit": int(flask.request.args.get("limit", 20))
    }


def get_task_list_params():
    return {
        "no_deadline": bool(flask.request.args.get("no_deadline", False))
    }
