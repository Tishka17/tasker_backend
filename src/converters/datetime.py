#!/usr/bin/env python
# -*- coding: utf-8 -*-
import typing

import dateutil.parser
import datetime


def from_str(date_str: str) -> typing.Optional[datetime.datetime]:
    if not date_str:
        return
    return dateutil.parser.parse(date_str)
