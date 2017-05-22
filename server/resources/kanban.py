from flask_restful import Resource, abort

from ..database import load


class User(Resource):
    def get(self, username):
        return load.user(username) or abort(404)


class Board(Resource):
    def get(self, board_id):
        return load.board(board_id) or abort(404)


class Lanes(Resource):
    def get(self, board_id):
        return load.lanes(board_id) or abort(404)
