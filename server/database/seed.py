import os
import json
import datetime

from .connector import db


def date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000Z")


def sample():
    folder = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(folder, 'data')
    for datafile in os.listdir(path):
        name, extension = datafile.split('.')
        if extension == 'json':
            filepath = os.path.join(path, datafile)
            with open(filepath) as data:
                data = json.load(data)
            if name == 'cards':
                for card in data:
                    for field in ['LastMove', 'DateArchived', 'LastActivity']:
                        if card[field]:
                            card[field] = date(card[field])
            elif name == 'events':
                for event in data:
                    event['DateTime'] = date(event['DateTime'])
            db[name].drop()
            if data:
                print("Populating {} {}".format(len(data), name.replace('_', ' ')))
                db[name].insert_many(data)
