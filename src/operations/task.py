#!/usr/bin/env python
# -*- coding: utf-8 -*-
import model.task


def update(orig: model.task.Task, new: model.task.Task) -> model.task.Task:
    orig.title = new.title
    orig.description = new.title
    orig.deadline = new.deadline
    orig.priority = new.priority
    orig.subscribers_visibility = new.subscribers_visibility
    orig.public_visibility = new.public_visibility
    return orig


def start(task: model.task.Task) -> model.task.Task:
    task.state = model.task.State.started
    return task


def pause(task: model.task.Task) -> model.task.Task:
    task.state = model.task.State.paused
    return task


def finish(task: model.task.Task) -> model.task.Task:
    task.state = model.task.State.finished
    return task
