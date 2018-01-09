from json import loads
from unittest import TestCase

from test import APITestCase
from api.user import UserModel


class TestUserModel(TestCase):
    @staticmethod
    def test_query(self):
        user = UserModel({"UserName": "User@example.org"})
        expected = [{"$match": {"UserName": "user@example.org",
                                "Password": {"$exists": False}}},
                    {"$lookup": {"from": "boards", "localField": "BoardId",
                                 "foreignField": "Id", "as": "Board"}}]
        assert user.query == expected


class TestUserHandler(APITestCase):
    url = "/api/user"

    def test_get_user(self):
        response = self.post({"UserName": "User1@example.org"})
        user = loads(response.body)
        assert response.code == 200
        assert user["FullName"] == "User 1"
        assert len(user["Boards"]) == 2

    def test_user_not_found(self):
        response = self.post({"UserName": "User3@example.org"})
        assert response.code == 404
