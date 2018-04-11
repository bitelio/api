from json import loads

from test import BaseTestCase


class TestLoginHandler(BaseTestCase):
    url = "/api/login"

    def test_successful_login(self):
        body = {"UserName": "User1@example.org ", "Password": "xxx"}
        response = self.post(body)
        assert response.code == 200
        body = loads(response.body)
        assert "token" in body
        redis = self._app.settings["redis"]
        assert redis.exists(f"session:{body['token']}")

    def test_wrong_username(self):
        body = {"UserName": "user3@example.org ", "Password": "xxx"}
        response = self.post(body)
        assert response.code == 404

    def test_wrong_password(self):
        body = {"UserName": "user1@example.org ", "Password": "ooo"}
        response = self.post(body)
        assert response.code == 401

    def test_bad_request(self):
        response = self.post(body={})
        assert response.code == 400
