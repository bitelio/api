#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.exceptions import DataError
from flask_restful import Resource
from flask_restful import abort
from flask import request

from .. import database
from ..schemas import models


class Base(Resource):
    @property
    def name(self):
        return self.__class__.__name__.lower()

    @staticmethod
    def not_found(board_id):
        abort(404, message="Board {} not found".format(board_id))


class Collection(Base):
    sorting = None

    def get(self, board_id):
        data = database.load.collection(self.name, board_id, self.sorting)
        if data or database.check.exists('boards', board_id):
            return data
        else:
            self.not_found(board_id)


class Group(Collection):
    def post(self, board_id):
        database.check.exists('boards', board_id) or self.not_found(board_id)
        payload = self.validate(request.get_json(force=True), board_id)
        database.remove.collection(self.name, board_id)
        if database.save.collection(self.name, payload):
            return payload, 201
        else:
            return abort(500, "Couldn't write to database")

    def validate(self, data, board_id):
        for item in data:
            if item['BoardId'] != board_id:
                abort(400, message="Board id doesn't match")
            try:
                self.model(item).validate()
            except DataError as error:
                abort(400, message=str(error))
        if not database.check.exists('boards', board_id):
            abort(400, message="Board {} not found".format(board_id))
        return data


class User(Resource):
    def get(self, username):
        return database.load.user(username) or \
            abort(404, message="User {} not found".format(username))


class Board(Base):
    def get(self, board_id):
        return database.load.board(board_id) or self.not_found(board_id)


class Settings(Base):
    def get(self, board_id):
        return database.load.document('settings', board_id) or \
            self.not_found(board_id)


class Lanes(Collection):
    """ Returns a list of lanes """


class Stations(Group):
    sorting = "Position"
    model = models.Station

    def validate(self, data, board_id):
        super(Stations, self).validate(data, board_id)
        lanes = [lane for station in data for lane in station['Lanes']]
        if len(lanes) != len(set(lanes)):
            abort(400, message="Station contains duplicate lane")
        stored = database.load.collection('lanes', board_id, {'Id': 1})
        lane_ids = [lane['Id'] for lane in stored]
        if set(lanes) - set(lane_ids):
            abort(400, message="Station contains wrong lane id")
        for position, station in enumerate(data, start=1):
            station['Position'] = position
        return data


class Phases(Group):
    sorting = "Position"
    model = models.Phase

    def validate(self, data, board_id):
        super(Phases, self).validate(data, board_id)
        stations = [station for phase in data for station in phase['Stations']]
        if len(stations) != len(set(stations)):
            abort(400, message="Phase contains duplicate station")
        stored = database.load.collection('stations', board_id, {'_id': 1})
        lane_ids = [station['_id'] for station in stored]
        if set(stations) - set(lane_ids):
            abort(400, message="Phase contains wrong station id")
        for position, phase in enumerate(data, start=1):
            phase['Position'] = position
        return data
