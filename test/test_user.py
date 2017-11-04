from json import loads
from unittest import TestCase

from . import APITestCase
from api.handlers.user import UserModel


class TestUserHandler(APITestCase):
    url = "/user"
    seed = ["users", "boards"]

    def test_post(self):
        response = self.post({"UserName": "User1@example.org"})
        user = loads(response.body)
        assert response.code == 200
        assert user["FullName"] == "User 1"
        assert len(user["Boards"]) == 2

    def test_not_found(self):
        response = self.post({"UserName": "User3@example.org"})
        assert response.code == 404


class TestUserModel(TestCase):
    def test_query(self):
        user = UserModel({"UserName": "User@example.org"})
        expected = [{"$match": {"UserName": "user@example.org"}},
                    {"$lookup": {"from": "boards", "localField": "BoardId",
                                 "foreignField": "Id", "as": "Board"}}]
        assert user.query == expected
