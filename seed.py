import os
import json

from server.database.connector import db


for datafile in os.listdir('data'):
    name, extension = datafile.split('.')
    if extension == 'json':
        with open('data/' + datafile) as data:
            data = json.load(data)
        db[name].drop()
        if data:
            print("Populating {} {}".format(len(data), name.replace('_', ' ')))
            db[name].insert_many(data)
