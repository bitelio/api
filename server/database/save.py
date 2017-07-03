#!/usr/bin/python
# -*- coding: utf-8 -*-

from .connector import db


def collection(collection, data):
    try:
        db[collection].insert_many(data)
        for item in data:
            item['_id'] = str(item['_id'])
        return data
    except TypeError:
        return False
