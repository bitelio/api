from json import loads
from pytest import mark

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

    @restore("accounts")
    def test_update_account(self):
        response = self.post({"Subscriptions": {"Updates": True}})
        assert response.code == 200
        body = loads(response.body)
        assert body["message"]["nModified"] == 1

    @restore("accounts")
    def test_change_password(self):
        response = self.post({"Password": "123456"})
        assert response.code == 200
        body = loads(response.body)
        assert body["message"]["nModified"] == 1

    @mark.skip(reason="Racing conditions")
    @restore("accounts")
    def test_delete_account(self):
        response = self.delete()
        assert response.code == 200
        cursor = self._app.settings["mongo"].accounts.find()
        assert len(cursor.to_list(None)) == 0
