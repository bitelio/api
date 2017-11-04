from json import loads
from unittest import TestCase

from . import APITestCase
from api.handlers.lanes import LanesModel


class TestLanesHandler(APITestCase):
    url = "/board/lanes"
    seed = ["lanes"]

    def test_post(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 12

    def test_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404

    def test_wip_lanes(self):
        response = self.post({"BoardId": 100000000, "Stage": "wip"})
        assert response.code == 200
        assert len(loads(response.body)) == 10


class TestLanesModel(TestCase):
    def test_query(self):
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query
