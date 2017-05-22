from .connector import db


def board(board_id):
    board = db.boards.find_one({'Id': board_id}, {'_id': 0})
    if board:
        board['CardTypes'] = _get_all_('card_types', board_id)
        board['ClassesOfService'] = _get_all_('classes_of_service', board_id)
        board['Settings'] = _get_one_('settings', board_id)
    return board


def lanes(board_id):
    return _get_all_('lanes', board_id)


def cards(board_id, history=True):
    cards = {card['Id']: card for card in _get_all_('cards', board_id)}
    if history:
        for event in events(board_id):
            card = cards[event['CardId']]
            if 'History' in card:
                card['History'].append(event)
            else:
                card['History'] = [event]
    return list(cards.values())


def events(board_id):
    return db.events.find({'BoardId': board_id}, {'_id': 0}).sort('Position')


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


def _get_all_(collection, board_id):
    return list(db[collection].find({'BoardId': board_id}, {'_id': 0}))


def _get_one_(collection, board_id):
    return db[collection].find_one({'BoardId': board_id}, {'_id': 0})
