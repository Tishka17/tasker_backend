#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum

from . import db


@enum.unique
class Visibility(enum.Enum):
    full = "full"
    title_only = "title_only"
    presence_only = "presence_only"
    invisible = "invisible"


SqlVisibility = db.Enum(Visibility)
