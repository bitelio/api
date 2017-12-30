from json import loads
from pytest import raises
from unittest import TestCase
from schematics.exceptions import DataError

from test import APITestCase
from api.board import BoardModel


class TestBoardModel(TestCase):
    @staticmethod
    def test_query():
        board = BoardModel({"BoardId": 100000000})
        assert len(board.query) == 4

    @staticmethod
    def test_bad_query():
        with raises(DataError):
            BoardModel(validate=True)

    @staticmethod
    def test_projection():
        expected = {"Id": 1, "Title": 1, "_id": 0, "AvailableTags": 1,
                    "CardTypes.Id": 1, "CardTypes.Ignore": 1,
                    "CardTypes.Name": 1, "ClassesOfService.Ignore": 1,
                    "ClassesOfService.Id": 1, "ClassesOfService.Title": 1}
        assert BoardModel().projection == expected


class TestBoardHandler(APITestCase):
    url = "/api/board"

    def test_get_board(self):
        response = self.post({"BoardId": 100000000})
        body = loads(response.body)
        assert response.code == 200
        assert body["Title"] == "Board 100000000"
        assert len(body["CardTypes"]) == 5
        assert len(body["ClassesOfService"]) == 4

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404
