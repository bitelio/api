import os
import json
import datetime

from server.database.connector import db


def date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000Z")


for datafile in os.listdir('data'):
    name, extension = datafile.split('.')
    if extension == 'json':
        with open('data/' + datafile) as data:
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
