from flask_restful import Resource, abort

from ..database import user, board, lanes


class User(Resource):
    def get(self, username):
        return user.get(username) or abort(404)


class Board(Resource):
    def get(self, board_id):
        return board.get(board_id) or abort(404)


class Lanes(Resource):
    def get(self, board_id):
        return lanes.get(board_id) or abort(404)
