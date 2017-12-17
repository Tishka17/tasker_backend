#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime


def from_str(strdate):
    return datetime.datetime.strptime(strdate, "%Y-%m-%dT%H:%M:%S")
