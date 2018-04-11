from pytest import raises
from schematics.exceptions import DataError

from api.models.board import StationModel, StationsModel


class TestStationModel:
    def test_include_fields(self):
        data = {"Name": "Station", "Lanes": [100001001]}
        model = StationModel(data, validate=True).to_native()
        data.update({"Card": 0, "Size": 0, "Phase": None})
        assert model == data

    def test_missing_name(self):
        with raises(DataError):
            StationModel({}, validate=True)


class TestStationsModel:
    def test_stations_model(self):
        StationsModel([], validate=True)

    def test_duplicate_lanes(self):
        data = [{"Name": "Station", "Lanes": [1, 1]}]
        with raises(DataError):
            StationsModel(data, validate=True)
