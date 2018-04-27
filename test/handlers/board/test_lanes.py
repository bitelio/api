from json import loads

from test import BaseTestCase
from test.mixins import BoardMixin


class TestLanesHandler(BoardMixin, BaseTestCase):
    url = "/api/100000000/lanes"

    def test_get_lanes(self):
        response = self.get()
        assert response.code == 200
        lanes = loads(response.body)
        assert len(lanes) == 12
