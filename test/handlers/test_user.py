from json import loads

from test import BaseTestCase, restore
from test.mixins import AuthMixin


class TestUserHandler(AuthMixin, BaseTestCase):
    url = "/api/user"

    def test_get_user(self):
        response = self.get()
        assert response.code == 200
        body = loads(response.body)
        assert len(body["Boards"]) == 2
        assert "Password" not in body

    @restore("users")
    def test_update_user(self):
        response = self.post({"Subscriptions": {"Updates": True}})
        assert response.code == 200
        body = loads(response.body)
        assert body["message"]["nModified"] == 1

    @restore("users")
    def test_change_password(self):
        response = self.post({"Password": "123456"})
        assert response.code == 200
        body = loads(response.body)
        assert body["message"]["nModified"] == 1
