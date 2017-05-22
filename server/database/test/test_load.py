from unittest import TestCase

from .. import load


class Load(TestCase):
    def test_get_board(self):
        data = load.board(100000000)
        self.assertIn('CardTypes', data)
        self.assertIn('ClassesOfService', data)

    def test_board_not_found(self):
        data = load.board(300000000)
        self.assertIsNone(data)

    def test_get_lanes(self):
        data = load.lanes(100000000)
        self.assertEqual(10, len(data))

    def test_lanes_not_found(self):
        data = load.lanes(300000000)
        self.assertEqual([], data)

    def test_get_cards(self):
        data = load.cards(100000000)
        self.assertEqual(3, len(data))
        self.assertIn('History', data[0])

    def test_get_cards_without_history(self):
        data = load.cards(100000000, history=False)
        self.assertEqual(3, len(data))
        self.assertNotIn('History', data[0])

    def test_get_cards_not_found(self):
        data = load.cards(300000000)
        self.assertEqual([], data)

    def test_get_user_by_email(self):
        data = load.user('user@example.org')
        self.assertDictContainsSubset({'UserName': 'user@example.org'}, data)

    def test_get_user_by_id(self):
        data = load.user(123456789)
        self.assertDictContainsSubset({'Id': 123456789}, data)

    def test_user_not_found(self):
        data = load.user('bogus@example.org')
        self.assertIsNone(data)
