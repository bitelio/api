from json import loads
from unittest import TestCase

from test import APITestCase
from api.board.lanes import LanesModel, LanesHandler


class TestLanesModel(TestCase):
    @staticmethod
    def test_query():
        query = {"BoardId": 100000000, "Stage": "wip"}
        lanes = LanesModel(query)
        assert lanes.query == query


class TestLanesHandler(APITestCase):
    url = "/api/board/lanes"

    def test_get_lanes(self):
        response = self.post({"BoardId": 100000000})
        assert response.code == 200
        assert len(loads(response.body)) == 4

    def test_board_not_found(self):
        response = self.post({"BoardId": 300000000})
        assert response.code == 404

    def test_arrange_lanes(self):
        lanes = [
          {"Id": 1, "Index": 0, "ParentLaneId": None, "ChildLaneIds": [2, 3]},
          {"Id": 2, "Index": 0, "ParentLaneId": 1, "ChildLaneIds": []},
          {"Id": 3, "Index": 0, "ParentLaneId": 1, "ChildLaneIds": [4]},
          {"Id": 4, "Index": 0, "ParentLaneId": 3, "ChildLaneIds": []},
          {"Id": 5, "Index": 0, "ParentLaneId": None, "ChildLaneIds": []}
        ]
        expected = [
          {"Id": 1, "Index": 0, "ParentLaneId": None, "ChildLanes": [
              {"Id": 2, "Index": 0, "ParentLaneId": 1, "ChildLanes": []},
              {"Id": 3, "Index": 0, "ParentLaneId": 1, "ChildLanes": [
                {"Id": 4, "Index": 0, "ParentLaneId": 3, "ChildLanes": []},
              ]},
          ]},
          {"Id": 5, "Index": 0, "ParentLaneId": None, "ChildLanes": []}
        ]
        result = LanesHandler.arrange(lanes)
        assert result == expected
