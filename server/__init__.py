#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask_restful import Api

from . import config
from .resources import kanban


__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = '0.0.1'


def run():  # pragma: no cover
    global app
    app.run()


app = flask.Flask(__name__)
app.config.from_object(config)
api = Api(app, catch_all_404s=True)
api.add_resource(kanban.User, '/user/<username>', endpoint='user')
api.add_resource(kanban.Board, '/board/<path:path>', endpoint='board')
