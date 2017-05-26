from flask_restful import Resource, reqparse

from ..kanban import Board
from .. import analytics


parser = reqparse.RequestParser()
parser.add_argument('Priority', action='append')
parser.add_argument('From')
parser.add_argument('To')


class Stations(Resource):
    def get(self, board_id):
        board = Board(board_id)
        return analytics.stations(board, parser.parse_args())
