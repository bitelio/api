from test import BaseTestCase

from test.mixins import AuthMixin


class TestLogoutHandler(AuthMixin, BaseTestCase):
    url = "/api/logout"

    def test_successful_logout(self):
        redis = self._app.settings["redis"]
        redis.set(f"session:+++", '{"UserName": "user@example.org"}')
        response = self.get(headers={"Cookie": "token=+++"})
        assert response.code == 200
        assert not redis.exists(f"session:+++")
