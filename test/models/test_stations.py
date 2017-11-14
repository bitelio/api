from pytest import raises
from unittest import TestCase
from schematics.exceptions import DataError

from api.models.stations import StationsModel


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
