import unittest

from server import app


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_user(self):
        response = self.app.get('/user/user@example.org')
        self.assertEqual(200, response.status_code)

    def test_user_not_found(self):
        response = self.app.get('/user/bogus@example.org')
        self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main()
