from json import loads
from unittest import TestCase

from . import APITestCase
from api.handlers.lanes import LanesModel


class TestLanesHandler(APITestCase):
    seed = ["lanes"]

    def test_get_lanes(self):
        response = self.post("/board/lanes", {"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 12

    def test_wrong_board(self):
        response = self.post("/board/lanes", {"BoardId": 300000000})
        assert response.code == 404

    def test_get_wip_lanes(self):
        body = {"BoardId": 100000000, "Stage": "wip"}
        response = self.post("/board/lanes", body)
        assert response.code == 200
        assert len(loads(response.body)) == 10


class TestLanesModel(TestCase):
    def test_lanes_query(self):
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query
