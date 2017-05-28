import flask
from flask_restful import Api

from . import config
from .resources import kanban


def run():
    global app
    app.run()


app = flask.Flask(__name__)
app.config.from_object(config)
api = Api(app, catch_all_404s=True)
api.add_resource(kanban.User, '/user/<username>', endpoint='user')
api.add_resource(kanban.Stats, '/board/<int:board_id>/averages')
# api.add_resource(kanban.Board, '/board/<path:path>', endpoint='board')
