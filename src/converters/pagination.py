#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask_sqlalchemy


def to_dict(pagination: flask_sqlalchemy.Pagination):
    return {
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "pages": pagination.pages,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "prev_num": pagination.prev_num,
        "next_num": pagination.next_num,
    }
