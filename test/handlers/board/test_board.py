from json import loads

from test import BaseTestCase
from test.mixins import BoardMixin


class TestBoardHandler(BoardMixin, BaseTestCase):
    url = "/api/100000000"

    def test_get_board(self):
        response = self.get()
        assert response.code == 200
        board = loads(response.body)
        expected = {"AvailableTags": "Tag1,Tag2", "Timezone": "Europe/Berlin",
                    "Update": True, "OfficeHours": ["8:00", "16:00"],
                    "Holidays": ["2017-05-01"]}
        assert board == expected
