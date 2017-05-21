from unittest import TestCase

from .. import board


class Board(TestCase):
    def test_get_board(self):
        data = board.get(100000000)
        self.assertIn('CardTypes', data)
        self.assertIn('ClassesOfService', data)

    def test_board_not_found(self):
        data = board.get(300000000)
        self.assertIsNone(data)
