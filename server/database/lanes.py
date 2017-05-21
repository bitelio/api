from .connector import db


def get(board_id):
    return list(db.lanes.find({'BoardId': board_id}, {'_id': 0})) or None
