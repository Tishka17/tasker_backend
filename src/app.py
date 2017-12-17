#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
import model
import init

import api.user
import api.authorization

import render.json_encoder

DEBUG = True  # FIXME remove in production

app = flask.Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'super-secret'  # FIXME generate on first start
app.config['JWT_AUTH_URL_RULE'] = None
app.json_encoder = render.json_encoder.CustomJSONEncoder

model.db.init_app(app)
model.db.app = app

api.authorization.jwt.init_app(app)
api.authorization.jwt.app = app

init.deploy(app)

app.register_blueprint(api.user.blueprint, url_prefix="/api/v1/users")
app.register_blueprint(api.authorization.blueprint, url_prefix="/api/v1/auth")

if __name__ == "__main__":
    app.run()
