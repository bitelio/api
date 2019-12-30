from rapidjson import loads
from test import BaseTestCase

from api.services import Services
from api.models import Session


class TestLoginHandler(BaseTestCase):
    url = "/api/login"

    def test_successful_login(self):
        body = {"username": "admin", "password": "xxx"}
        response = self.post(body)
        assert response.code == 200
        body = loads(response.body)
        assert "token" in body
        assert Services.redis.exists(f"{body['token']}")
        session = Session.get(body['token'])
        assert session.username == 'admin'
        assert session.role == 3

    def test_wrong_username(self):
        body = {"username": "user", "password": "xxx"}
        response = self.post(body)
        assert response.code == 401

    def test_wrong_password(self):
        body = {"username": "guest", "password": "ooo"}
        response = self.post(body)
        assert response.code == 401

    def test_bad_request(self):
        response = self.post(body={"username": "guest"})
        assert response.code == 400


class TestLogoutHandler(BaseTestCase):
    url = "/api/logout"

    def test_successful_logout(self):
        response = self.get(auth=True)
        assert response.code == 200
        response = self.get(auth=True)
        assert response.code == 401

    def test_missing_token(self):
        response = self.get()
        assert response.code == 401
