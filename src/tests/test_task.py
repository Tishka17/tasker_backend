#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import flask

import model
import model.user
import model.task


class Test1(unittest.TestCase):
    app = None

    def setUp(self):
        super().setUp()

        app = flask.Flask(__name__)
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        model.db.init_app(app)
        app.app_context().push()
        with app.app_context():
            model.db.create_all()
        self.app = app

    def tearDown(self):
        super().tearDown()
        model.db.session.remove()
        model.db.drop_all()

    def test_create(self):
        user = model.user.User(login="root")
        user.name = "TestName"
        task = model.task.Task(owner=user, title="TestTitle")
        model.db.session.add(user)
        model.db.session.add(task)

        self.assertEqual(len(model.user.User.query.all()), 1)
        self.assertEqual(len(model.task.Task.query.all()), 1)

    def test_delete(self):
        user = model.user.User(login="root")
        user.name = "TestName"
        task = model.task.Task(owner=user, title="TestTitle")
        model.db.session.add(user)
        model.db.session.add(task)
        model.db.session.commit()
        model.db.session.delete(user)

        self.assertEqual(len(model.user.User.query.all()), 0)
        self.assertEqual(len(model.task.Task.query.all()), 0)
