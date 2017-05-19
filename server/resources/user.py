from flask_restful import Resource, abort

from ..database import user


class User(Resource):
    def get(self, username):
        return user.get(username) or abort(404)
