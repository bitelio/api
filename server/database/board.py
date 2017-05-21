from .connector import db


def get(board_id):
    board = db.boards.find_one({'Id': board_id}, {'_id': 0})
    if board:
        query = ({'BoardId': board_id}, {'_id': 0})
        board['CardTypes'] = list(db.card_types.find(*query))
        board['ClassesOfService'] = list(db.classes_of_service.find(*query))
    return board
