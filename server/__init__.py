import flask
from flask_restful import Api

from . import config
from .resources import kanban


app = flask.Flask(__name__)
app.config.from_object(config)
api = Api(app, catch_all_404s=True)
api.add_resource(kanban.User, '/user/<username>', endpoint='user')
api.add_resource(kanban.Board, '/board/<int:board_id>', endpoint='board')
