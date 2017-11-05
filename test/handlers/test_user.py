from json import loads

from . import APITestCase


class TestUserHandler(APITestCase):
    url = "/user"

    def test_post(self):
        response = self.post({"UserName": "User1@example.org"})
        user = loads(response.body)
        assert response.code == 200
        assert user["FullName"] == "User 1"
        assert len(user["Boards"]) == 2

    def test_not_found(self):
        response = self.post({"UserName": "User3@example.org"})
        assert response.code == 404
