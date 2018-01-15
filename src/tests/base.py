#!/usr/bin/env python
# -*- coding: utf-8 -*-
import flask

import model


def create_app(name):
    app = flask.Flask(name)
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    model.db.init_app(app)
    app.app_context().push()
    with app.app_context():
        model.db.create_all()