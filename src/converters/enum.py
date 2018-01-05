#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.enum


def to_str(v):
    if not v:
        return None
    else:
        return v.value


def from_str(cls, s):
    if not s:
        return None
    else:
        return cls(s)
