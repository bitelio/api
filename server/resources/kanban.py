from flask_restful import Resource, abort

from .. import config
from .. import database


class User(Resource):
    @staticmethod
    def get(username):
        return database.load.user(username) or abort(404)


class Board(Resource):
    items = ['lanes', 'users', 'card_types', 'classes_of_service']

    def get(self, path):
        attrs = path.strip('/').split('/')
        board_id = int(attrs[0])
        if len(attrs) == 1:
            return database.load.board(board_id) or abort(404)
        elif len(attrs) == 2:
            collection = attrs[1]
            if collection in self.items:
                return database.load.collection(collection, board_id)
            elif collection in config.COLLECTIONS:
                data = database.load.collection(collection, board_id)
                if data or database.check.exists('boards', board_id):
                    return data
        return abort(404)
