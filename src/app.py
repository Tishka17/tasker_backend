#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
import model

import init
import config

import api
import pages
import use_cases.authorization

import converters.json_encoder

DEBUG = True  # FIXME remove in production

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'super-secret'  # FIXME generate on first start
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['VK_SECRET_KEY'] = config.secret_key
app.config['VK_CLIENT_ID'] = config.client_id

app.json_encoder = converters.json_encoder.CustomJSONEncoder

model.db.init_app(app)
model.db.app = app

use_cases.authorization.jwt.init_app(app)
use_cases.authorization.jwt.app = app

init.deploy(app)

app.register_blueprint(api.blueprint, url_prefix="/api/v1")
app.register_blueprint(pages.blueprint)

if __name__ == "__main__":
    app.run()
