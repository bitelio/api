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
    roles = {1: 'reader', 2: 'user', 3: '-', 4: 'administrator'}
    field = 'Id' if isinstance(user, int) else 'UserName'
    pipeline = [{'$match': {field: user}},
                {'$lookup': {'from': 'boards', 'localField': 'BoardId',
                             'foreignField': 'Id', 'as': 'Board'}}]
    matches = list(db.users.aggregate(pipeline))

    if matches:
        user = {key: matches[0][key] for key in ['Id', 'FullName', 'UserName']}
        user['Boards'] = []
        for match in matches:
            user['Boards'].append({'BoardId': match['BoardId'],
                                   'BoardTitle': match['Board'][0]['Title'],
                                   'Enabled': match['Enabled'],
                                   'Role': roles[match['Role']]})
        return user
    else:
        return None


def settings(board_id):
    return db.settings.find_one({'BoardId': board_id}, {'_id': 0})
