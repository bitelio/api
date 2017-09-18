from flask_restful import abort

from .. import database
from .. import handlers
from ..schemas import models


class User(handlers.Resource):
    @staticmethod
    def get(username):
        return database.load.user(username) or \
            abort(404, message="User {} not found".format(username))


class Board(handlers.Base):
    def get(self, board_id):
        return database.load.board(board_id) or self.not_found(board_id)


class Settings(handlers.Base):
    def get(self, board_id):
        return database.load.document('settings', board_id) or \
            self.not_found(board_id)


class Lanes(handlers.Collection):
    """ Returns a list of lanes """


class Stations(handlers.Group):
    model = models.Station
    sorting = "Position"

    def validate(self, data, board_id):
        super().validate(data, board_id)
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


class Phases(handlers.Group):
    model = models.Phase

    def validate(self, data, board_id):
        super().validate(data, board_id)
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
