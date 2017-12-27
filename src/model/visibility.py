#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum


@enum.unique
class Visibility(enum.Enum):
    full = "full"
    title_only = "title_only"
    presence_only = "presence_only"
    invisible = "invisible"