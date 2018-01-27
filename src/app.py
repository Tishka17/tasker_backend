#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask

import model
import os
import init
import api
import pages
import use_cases.authorization
import converters.json_encoder

DEBUG = bool(os.environ.get('VK_SECRET_KEY'))

app = flask.Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['VK_SECRET_KEY'] = os.environ['VK_SECRET_KEY']
app.config['VK_CLIENT_ID'] = os.environ['VK_CLIENT_ID']
app.config['GOOGLE_SECRET_KEY'] = os.environ['GOOGLE_SECRET_KEY']
app.config['GOOGLE_CLIENT_ID'] = os.environ['GOOGLE_CLIENT_ID']
app.config["BASE_URL"] = os.environ['BASE_URL']


app.json_encoder = converters.json_encoder.CustomJSONEncoder
app.jinja_env.globals['url_for_other_page'] = pages.template_filters.url_for_other_page

model.db.init_app(app)
model.db.app = app

use_cases.authorization.csrf_protect.init_app(app)
use_cases.authorization.jwt.init_app(app)
use_cases.authorization.jwt.app = app

init.deploy(app)

app.register_blueprint(api.blueprint, url_prefix="/api/v1")
app.register_blueprint(pages.blueprint)

if __name__ == "__main__":
    app.run()
