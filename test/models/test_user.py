from unittest import TestCase

from api.models.user import UserModel


class TestUserModel(TestCase):
    def test_query(self):
        user = UserModel({"UserName": "User@example.org"})
        expected = [{"$match": {"UserName": "user@example.org"}},
                    {"$lookup": {"from": "boards", "localField": "BoardId",
                                 "foreignField": "Id", "as": "Board"}}]
        assert user.query == expected
