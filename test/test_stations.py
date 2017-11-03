from json import loads
from unittest import TestCase

from . import APITestCase
from api.handlers.stations import StationsModel


class TestStationsHandler(APITestCase):
    seed = ["stations"]

    def test_get_stations(self):
        response = self.post("/board/stations", {"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 4

    def test_wrong_board(self):
        response = self.post("/board/stations", {"BoardId": 300000000})
        assert response.code == 404


class TestStationsModel(TestCase):
    @classmethod
    def setUpClass(cls):
        data = {"BoardId": 100000000,
                "Stations": [{"Name": "Station 1", "Card": 1.5, "Size": 0.5,
                              "Phase": "Phase 1", "Lanes": [100001003]},
                             {"Name": "Station 2"}]}
        cls.model = StationsModel(data, method="PUT")

    def test_query(self):
        assert self.model.query == {"BoardId": 100000000}

    def test_projection(self):
        expected = {"Name": 1, "Lanes": 1, "Card": 1,
                    "Size": 1, "Phase": 1, "_id": 0}
        assert self.model.projection == expected

    def test_payload(self):
        expected = [{"Name": "Station 1", "Card": 1.5, "Size": 0.5,
                     "Phase": "Phase 1", "BoardId": 100000000, "Position": 0,
                     "Lanes": [100001003]},
                    {"Name": "Station 2", "Card": 0.0, "Size": 0.0,
                     "Phase": None, "BoardId": 100000000, "Position": 1,
                     "Lanes": []}]
        assert self.model.payload == expected
