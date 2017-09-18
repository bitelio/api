from collections import Counter
from schematics.exceptions import DataError
from flask_restful import Resource
from flask_restful import abort
from flask import request

from .. import database


class Base(Resource):
    @property
    def name(self):
        return self.__class__.__name__

    @staticmethod
    def not_found(board_id):
        abort(404, message="Board {} not found".format(board_id))


class Collection(Base):
    """ List of kanban items with unique ids """
    sorting = None

    def get(self, board_id):
        data = database.load.collection(self.name, board_id, self.sorting)
        if data or database.check.exists('boards', board_id):
            return data
        else:
            self.not_found(board_id)


class Group(Collection):
    """ List of sorted items """
    def post(self, board_id):
        if not database.check.exists('boards', board_id):
            self.not_found(board_id)
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

    def duplicate(self, data):
        items = [item for group in data for item in group[self.name]]
        duplicates = [key for key, value in Counter(items) if value > 1]
        if duplicates:
            abort(400, message=f"{self.name} has a duplicate: {duplicates[0]}")
        return items
