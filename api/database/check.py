from .connector import db


def exists(collection, value, key='Id'):
    return db[collection].find_one({key: value}) != None
