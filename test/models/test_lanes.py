from unittest import TestCase

from api.models.lanes import LanesModel


class TestLanesModel(TestCase):
    def test_query(self):
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query
