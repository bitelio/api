from .connector import db


def board(board_id):
    board = db.boards.find_one({'Id': board_id}, {'_id': 0})
    if board:
        board['CardTypes'] = card_types(board_id)
        board['ClassesOfService'] = classes_of_service(board_id)
        board['Settings'] = settings(board_id)
    return board


def lanes(board_id):
    return list(db.lanes.find({'BoardId': board_id}, {'_id': 0})) or None


def card_types(board_id):
    return list(db.card_types.find({'BoardId': board_id}, {'_id': 0}))


def classes_of_service(board_id):
    return list(db.classes_of_service.find({'BoardId': board_id}, {'_id': 0}))


def user(user):
    if isinstance(user, str):
        matches = list(db.users.find({'UserName': user}))
    elif isinstance(user, int):
        matches = list(db.users.find({'Id': user}))
    else:
        raise ValueError("Expected str or int; got {}".format(type(user)))

    if matches:
        keys = ['BoardId', 'Role', 'Enabled']
        user = {key: matches[0][key] for key in ['Id', 'FullName', 'UserName']}
        boards = [{key: match[key] for key in keys} for match in matches]
        user['Boards'] = boards
        return user
    else:
        return None


def settings(board_id):
    return db.settings.find_one({'BoardId': board_id}, {'_id': 0})
