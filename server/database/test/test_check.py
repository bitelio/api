from unittest import TestCase

from .. import check


class Load(TestCase):
    def test_board_exists(self):
        self.assertTrue(check.exists('boards', 100000000))

    def test_card_does_not_exists(self):
        self.assertFalse(check.exists('cards', 100000000))
