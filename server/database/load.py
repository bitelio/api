# -*- coding: utf-8 -*-

from .connector import db
from .mappings import roles


def collection(collection, board_id, query=None):
    fields = {'BoardId': board_id}
    fields.update(getattr(query, 'serialize', {}))
    return list(db[collection].find(fields, {'_id': 0}))


def document(collection, doc_id):
    return db[collection].find_one({'Id': doc_id}, {'_id': 0})


def kanban(board_id, query):
    board = document('boards', board_id)
    board['Settings'] = document('settings', board_id)
    board['Lanes'] = collection('lanes', board_id)
    board['Cards'] = collection('cards', board_id, query)
    return board


def board(board_id):
    board = db.boards.find_one({'Id': board_id}, {'_id': 0})
    if board:
        board['CardTypes'] = collection('card_types', board_id)
        board['ClassesOfService'] = collection('classes_of_service', board_id)
        board['Settings'] = document('settings', board_id)
    return board


def lanes(board_id):
    return collection('lanes', board_id)


def cards(board_id, history=True, query=None):
    cards = {card['Id']: card for card in collection('cards', board_id, query)}
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


def comments(card_id=None):
    query = {'Type': 'CommentPostEventDTO'}
    if card_id:
        query.update({'CardId': card_id})
    return list(db.events.find(query).sort('Position'))
