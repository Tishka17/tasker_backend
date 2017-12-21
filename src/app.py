#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
import model

import init

import api.user
import api.task
import api.authorization
import pages.login
import viewmodel.authorization

import converters.json_encoder

DEBUG = True  # FIXME remove in production

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'super-secret'  # FIXME generate on first start
app.config['JWT_AUTH_URL_RULE'] = None
app.json_encoder = converters.json_encoder.CustomJSONEncoder

model.db.init_app(app)
model.db.app = app

viewmodel.authorization.jwt.init_app(app)
viewmodel.authorization.jwt.app = app

init.deploy(app)

app.register_blueprint(api.user.blueprint, url_prefix="/api/v1/users")
app.register_blueprint(api.task.blueprint, url_prefix="/api/v1/tasks")
app.register_blueprint(api.authorization.blueprint, url_prefix="/api/v1/auth")
app.register_blueprint(pages.login.blueprint, url_prefix="/login")

if __name__ == "__main__":
    app.run()
