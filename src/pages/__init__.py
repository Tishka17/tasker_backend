#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .blueprint import blueprint
from . import user, logout, login, task, template_filters

__all__ = [
    "blueprint"
]
