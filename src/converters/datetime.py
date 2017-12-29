#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import dateutil.parser


def from_str(strdate):
    if not strdate:
        return
    return dateutil.parser.parse(strdate)
