from flask_restful import Resource, abort, reqparse

from .. import config
from ..database import load
from ..analytics import stations


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


class Stats(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('TypeId', action='append')
    parser.add_argument('Priority', action='append')

    def adapt(self, args):
        for key in args:
            args[key] = [int(i) for i in args[key]]
        return args

    def get(self, board_id):
        args = self.parser.parse_args()
        if args['TypeId'] or args['Priority']:
            args = self.adapt(args)
        else:
            args = {}
        return stations.averages(board_id, args)
