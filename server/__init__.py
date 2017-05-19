import flask
from flask_restful import Api

from . import config
from .resources import user


app = flask.Flask(__name__)
app.config.from_object(config)
api = Api(app, catch_all_404s=True)
api.add_resource(user.User, '/user/<username>', endpoint='user')
