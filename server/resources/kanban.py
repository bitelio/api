from flask_restful import Resource, abort

from .. import config
from ..database import load


class User(Resource):
    def get(self, username):
        return load.user(username) or abort(404)


class Board(Resource):
    items = ['lanes', 'users', 'card_types', 'classes_of_service']

    def get(self, path):
        attrs = path.strip('/').split('/')
        board_id = int(attrs[0])
        if len(attrs) == 1:
            return load.board(board_id) or abort(404)
        elif len(attrs) == 2:
            collection = attrs[1]
            if collection in self.items + config.COLLECTIONS:
                return load._get_all_(collection, board_id)
        return abort(404)
