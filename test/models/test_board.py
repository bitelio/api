from pytest import raises
from schematics.exceptions import DataError

from api.models.board import StationModel, StationsModel


class TestStationModel:
    @staticmethod
    def test_include_fields():
        data = {"Name": "Station", "Lanes": [100001001]}
        model = StationModel(data, validate=True).to_native()
        data.update({"Card": 0, "Size": 0, "Phase": None})
        assert model == data

    @staticmethod
    def test_missing_name():
        with raises(DataError):
            StationModel({}, validate=True)


class TestStationsModel:
    @staticmethod
    def test_stations_model():
        StationsModel([], validate=True)

    @staticmethod
    def test_duplicate_lanes():
        data = [{"Name": "Station", "Lanes": [1, 1]}]
        with raises(DataError):
            StationsModel(data, validate=True)
