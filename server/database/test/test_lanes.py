from unittest import TestCase

from .. import lanes


class Lanes(TestCase):
    def test_get_lanes(self):
        data = lanes.get(100000000)
        self.assertEqual(10, len(data))

    def test_lanes_not_found(self):
        data = lanes.get(300000000)
        self.assertIsNone(data)
