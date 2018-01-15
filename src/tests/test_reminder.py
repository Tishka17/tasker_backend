#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import model
import model.reminder
import model.task
import model.enum
import model.user

import use_cases.task
import use_cases.user

from . import base


class Test(unittest.TestCase):
    root = None
    user = None
    app = None

    def setUp(self):
        self.app = base.create_app(self._testMethodName)
        self.root = model.user.User(
            login="root2",
            public_visibility=model.enum.Visibility.full,
            subscribers_visibility=model.enum.Visibility.full
        )
        self.user = model.user.User(
            login="user2",
            public_visibility=model.enum.Visibility.full,
            subscribers_visibility=model.enum.Visibility.full
        )
        model.db.session.add(self.root)
        model.db.session.add(self.user)
        model.db.session.commit()

    def test_get(self):
        comment = "Comment"
        task = model.task.Task(
            title="Title"
        )

        use_cases.task.create(self.root.id, task)
        reminder = use_cases.task.remind(self.user.id, task.id, comment)

        sent = use_cases.user.get_sent_reminders(self.user.id).items
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0].id, reminder.id)
        self.assertEqual(sent[0].comment, comment)

        sent = use_cases.user.get_reminders(self.root.id).items
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0].id, reminder.id)
        self.assertEqual(sent[0].comment, comment)

        sent = use_cases.user.get_reminders(self.user.id).items
        self.assertEqual(len(sent), 0)
