#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import model
import model.user
import model.task

from . import base


class Test1(unittest.TestCase):
    app = None

    def setUp(self):
        super().setUp()
        self.app = base.create_app(self._testMethodName)

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
