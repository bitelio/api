from pytest import raises
from unittest import TestCase
from schematics.exceptions import DataError

from api.models.board import BoardModel


class TestBoardModel(TestCase):
    def test_query(self):
        board = BoardModel({"BoardId": 100000000})
        assert len(board.query) == 3

    def test_bad_query(self):
        with raises(DataError):
            BoardModel(validate=True)
