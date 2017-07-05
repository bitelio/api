#!/usr/bin/python
# -*- coding: utf-8 -*-

from .connector import db


def collection(collection, board_id):
    db[collection].remove({'BoardId': board_id})
