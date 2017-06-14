import unittest

from server import app
from server.database import seed


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        seed.sample()
        self.app = app.test_client()

    def test_get_user(self):
        response = self.app.get('/user/user@example.org')
        self.assertEqual(200, response.status_code)

    def test_user_not_found(self):
        response = self.app.get('/user/bogus@example.org')
        self.assertEqual(404, response.status_code)

    def test_get_board(self):
        response = self.app.get('/board/100000000')
        self.assertEqual(200, response.status_code)

    def test_board_not_found(self):
        response = self.app.get('/board/300000000')
        self.assertEqual(404, response.status_code)

    def test_get_lanes(self):
        response = self.app.get('/board/100000000/lanes')
        self.assertEqual(200, response.status_code)

    def test_lanes_not_found(self):
        response = self.app.get('/board/300000000/lanes')
        self.assertEqual(200, response.status_code)

    def test_stations(self):
        response = self.app.get('/board/100000000/stations')
        self.assertEqual(200, response.status_code)

    def test_stations_board_not_found(self):
        response = self.app.get('/board/300000000/stations')
        self.assertEqual(404, response.status_code)

    def test_board_collection_not_found(self):
        response = self.app.get('/board/100000000/bogus')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
