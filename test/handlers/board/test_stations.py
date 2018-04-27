from json import loads

from test import BaseTestCase, restore
from test.mixins import BoardMixin


class TestStationsHandler(BoardMixin, BaseTestCase):
    url = "/api/100000000/stations"

    def test_get_stations(self):
        response = self.get()
        assert response.code == 200
        lanes = loads(response.body)
        assert len(lanes) == 4

    @restore("stations")
    def test_post_stations(self):
        station = {"Name": "Station", "Lanes": [100001003]}
        response = self.post([station])
        assert response.code == 200
        station.update({"Card": 0.0, "Size": 0.0, "Phase": None})
        assert [station] == loads(response.body)

    def test_bad_request(self):
        response = self.post({})
        assert response.code == 400
