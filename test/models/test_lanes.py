from unittest import TestCase

from api.models.lanes import LanesModel


class TestLanesModel(TestCase):
    @staticmethod
    def test_query():
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query
