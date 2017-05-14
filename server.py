from flask import Flask
from flask_restful import Api

from . import config
from .resources.user import User


app = Flask(__name__)
api = Api(app)
app.config.from_object(config)

api.add_resource(User, '/user/<string:username>')


if __name__ == '__main__':
    app.run()
