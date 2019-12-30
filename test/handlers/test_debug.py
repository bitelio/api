from test import BaseTestCase
from unittest.mock import patch


class TestFastlaneHandler(BaseTestCase):
    url = "/api/fastlane"

    def test_debug_endpoint(self):
        response = self.get()
        assert response.code == 404
        with patch.dict(self._app.settings, {'debug': True}):
            response = self.get()
            assert response.code == 200
