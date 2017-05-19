from .connector import db


ROLES = {1: 'reader', 2: 'user', 3: '-', 4: 'administrator'}


def get(user):
    if isinstance(user, str):
        matches = list(db.users.find({'UserName': user}))
    elif isinstance(user, int):
        matches = list(db.users.find({'Id': user}))
    else:
        raise ValueError("Expected str or int; got {}".format(type(user)))

    if matches:
        boards = []
        for match in matches:
            boards.append({'BoardId': match['BoardId'],
                           'Role': ROLES[match['Role']],
                           'Enabled': match['Enabled']})
        user = {key: match[key] for key in ['Id', 'FullName', 'UserName']}
        user['Boards'] = boards
        return user
    else:
        return None
