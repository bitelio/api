from json import loads

from test import APITestCase


class TestSettingsHandler(APITestCase):
    url = "/api/board/settings"

    def test_get_settings(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 4

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404
