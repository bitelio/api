from json import loads
from pytest import raises
from unittest import TestCase
from schematics.exceptions import DataError

from test import APITestCase, restore
from api.board.stations import StationsModel


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

    def test_payload(self):
        expected = [{"Name": "Station 1", "Card": 1.5, "Size": 0.5,
                     "Phase": "Phase 1", "BoardId": 100000000, "Position": 0,
                     "Lanes": [100001003]},
                    {"Name": "Station 2", "Card": 0.0, "Size": 0.0,
                     "Phase": None, "BoardId": 100000000, "Position": 1,
                     "Lanes": []}]
        assert self.model.payload == expected

    @staticmethod
    def test_validation():
        data = {"BoardId": 100000000,
                "Stations": [{"Name": "Station 1", "Lanes": [100001003]},
                             {"Name": "Station 2", "Lanes": [100001003]}]}
        with raises(DataError):
            StationsModel(data, method="PUT", validate=True)


class TestStationsHandler(APITestCase):
    url = "/api/board/stations"

    def test_get_stations(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 4

    def test_get_no_stations(self):
        response = self.post({"BoardId": 200000000})
        assert response.code == 200
        assert len(loads(response.body)) == 0

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404

    @restore("stations")
    def test_put_stations(self):
        payload = {"BoardId": 200000000, "Stations": [{"Name": "Test"}]}
        response = self.put(payload)
        expected = [{"Name": "Test", "Position": 0, "BoardId": 200000000,
                     "Card": 0.0, "Size": 0.0, "Phase": None, "Lanes": []}]
        assert response.code == 200
        assert loads(response.body) == expected
        response = self.put({"BoardId": 200000000, "Stations": []})
        assert response.code == 200
        assert loads(response.body) == []

    def test_put_stations_and_fail(self):
        response = self.put({"BoardId": 200000000})
        assert response.code == 400
