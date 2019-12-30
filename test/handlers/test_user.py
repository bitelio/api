from rapidjson import loads
from test import BaseTestCase


class TestProfileHandler(BaseTestCase):
    url = "/api/profile"

    def test_get_profile(self):
        response = self.get(auth=True)
        assert response.code == 200
        body = loads(response.body)
        assert body == {
            "username": "admin",
            "email": "admin@bitelio.com",
            "role": 3,
        }

    def test_profile_auth(self):
        response = self.get()
        assert response.code == 401
