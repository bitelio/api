from json import loads
from unittest import TestCase

from test import APITestCase
from api.auth import AuthModel


class TestAuthModel(TestCase):
    @staticmethod
    def test_query():
        auth = AuthModel({"UserName": "User@example.org ", "Password": "xxx"})
        expected = {"UserName": "user@example.org",
                    "Password": {"$exists": True}}
        assert auth.query == expected


class TestAuthHandler(APITestCase):
    url = "/api/auth"

    def test_auth(self):
        response = self.post({"UserName": "User1@example.org",
                              "Password": "xxx"})
        auth = loads(response.body)
        assert response.code == 200
        assert auth["token"].isalnum()

    def test_user_not_found(self):
        response = self.post({"UserName": "User3@example.org",
                              "Password": "xxx"})
        assert response.code == 404

    def test_wrong_password(self):
        response = self.post({"UserName": "User1@example.org",
                              "Password": "123"})
        assert response.code == 401
