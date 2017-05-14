import os
import unittest

from ..server import app


class ServerTest(unittest.TestCase):
    def setUp(self):
        app.config['MONGO_URI'] += '-test'
        self.app = app.test_client()

    def tearDown(self):
        os.unlink(app.config['MONGO_URI'])


if __name__ == '__main__':
    unittest.main()
