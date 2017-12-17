#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user

import typing


def to_dict(user: model.user.User) -> dict:
    return {
        "id": user.id,
        "login": user.login,
        "name": user.name,
        "about": user.about,
        "registration_date": user.registration_date,
        "public_visibility": user.public_visibility,
        "subscribers_visibility": user.subscribers_visibility,
        "confirmed": user.confirmed,
        "blocked": user.blocked,
    }


def many_to_dict(users: typing.Iterable[model.user.User]) -> typing.Generator[dict, None, None]:
    return (to_dict(user) for user in users)
