from json import loads

from . import APITestCase


class TestBoardHandler(APITestCase):
    url = "/api/board"

    def test_get_board(self):
        response = self.post({"BoardId": 100000000})
        body = loads(response.body)
        assert response.code == 200
        assert body["Title"] == "Board 100000000"
        assert len(body["CardTypes"]) == 5
        assert len(body["ClassesOfService"]) == 4

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404
