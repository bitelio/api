from pytest import raises
from unittest import TestCase
from schematics.exceptions import DataError

from api.models.board import BoardModel


class TestBoardModel(TestCase):
    def test_query(self):
        board = BoardModel({"BoardId": 100000000})
        assert len(board.query) == 4

    def test_bad_query(self):
        with raises(DataError):
            BoardModel(validate=True)

    def test_projection(self):
        projection = {"Id": 1, "Title": 1, "_id": 0, "AvailableTags": 1,
                      "CardTypes.Id": 1, "CardTypes.Ignore": 1,
                      "CardTypes.Name": 1, "ClassesOfService.Ignore": 1,
                      "ClassesOfService.Id": 1, "ClassesOfService.Title": 1}
        assert BoardModel().projection == projection
