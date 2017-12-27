#!/usr/bin/env python
# -*- coding: utf-8 -*-


class NotFoundException(Exception):
    pass


class AccessDeniedException(Exception):
    pass


class InvalidCredentials(Exception):
    pass
