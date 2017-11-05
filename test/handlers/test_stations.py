from json import loads

from . import APITestCase, restore


class TestStationsHandler(APITestCase):
    url = "/board/stations"

    def test_post(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 4

    def test_no_stations(self):
        response = self.post({"BoardId": 200000000})
        assert response.code == 200
        assert len(loads(response.body)) == 0

    def test_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404

    @restore("stations")
    def test_put(self):
        payload = {"BoardId": 200000000, "Stations": [{"Name": "Test"}]}
        response = self.put(payload)
        expected = [{"Name": "Test", "Position": 0, "BoardId": 200000000,
                     "Card": 0.0, "Size": 0.0, "Phase": None, "Lanes": []}]
        assert response.code == 200
        assert loads(response.body) == expected
        response = self.put({"BoardId": 200000000, "Stations": []})
        assert response.code == 200
        assert loads(response.body) == []

    def test_put_fail(self):
        response = self.put({"BoardId": 200000000})
        assert response.code == 400

    def test_put_not_found(self):
        response = self.put({"BoardId": 300000000, "Stations": []})
        assert response.code == 404
