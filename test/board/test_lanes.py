from json import loads
from unittest import TestCase

from test import APITestCase
from api.board.lanes import LanesModel


class TestLanesModel(TestCase):
    @staticmethod
    def test_query():
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query


class TestLanesHandler(APITestCase):
    url = "/api/board/lanes"

    def test_get_lanes(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 12

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404

    # def test_wip_lanes(self):
        # response = self.post({"BoardId": 100000000, "Stage": "wip"})
        # assert response.code == 200
        # assert len(loads(response.body)) == 10
