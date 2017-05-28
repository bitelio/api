from .connector import db


def board(board_id):
    return db.boards.find_one({'Id': board_id}) != None
