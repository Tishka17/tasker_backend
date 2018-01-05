#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.user
import model.enum

from . import enum
import typing


def to_dict(user: model.user.User) -> dict:
    return {
        "id": user.id,
        "login": user.login,
        "name": user.name,
        "about": user.about,
        "registration_date": user.registration_date,
        "public_visibility": enum.to_str(user.public_visibility),
        "subscribers_visibility": enum.to_str(user.subscribers_visibility),
        "confirmed": user.confirmed,
        "blocked": user.blocked,
    }


def from_dict(dct):
    return model.user.User(
        login=dct.get("login"),
        name=dct.get("name"),
        about=dct.get("about"),
        subscribers_visibility=enum.from_str(model.enum.Visibility, dct.get("subscribers_visibility")),
        public_visibility=enum.from_str(model.enum.Visibility, dct.get("public_visibility"))
    )


def many_to_dict(users: typing.Iterable[model.user.User]) -> typing.Generator[dict, None, None]:
    return (to_dict(user) for user in users)
