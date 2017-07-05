#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask_restful import Api
from raven.contrib.flask import Sentry

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
api.add_resource(kanban.User, '/user/<string:username>')
api.add_resource(kanban.Board, '/board/<int:board_id>')
api.add_resource(kanban.Lanes, '/lanes/<int:board_id>')
api.add_resource(kanban.Phases, '/phases/<int:board_id>')
api.add_resource(kanban.Stations, '/stations/<int:board_id>')
api.add_resource(kanban.Settings, '/settings/<int:board_id>')

sentry = Sentry(app)
