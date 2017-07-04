#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import json
from .. import app
from ..database import seed


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed.sample()
        cls.app = app.test_client()

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
        response = self.app.get('/lanes/100000000')
        self.assertEqual(200, response.status_code)

    def test_lanes_not_found(self):
        response = self.app.get('/lanes/300000000')
        self.assertEqual(404, response.status_code)

    def test_stations(self):
        response = self.app.get('/stations/100000000')
        self.assertEqual(200, response.status_code)

    def test_stations_not_found(self):
        response = self.app.get('/stations/300000000')
        self.assertEqual(404, response.status_code)

    def test_post_stations(self):
        payload = [{'Position': 0, 'Title': 'Test',
                    'Lanes': [200000012], 'BoardId': 200000000}]
        response = self.app.post('/stations/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)
        stations = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(stations[0]['Position'], 1)

    def test_post_stations_with_wrong_board_id(self):
        payload = [{'Position': 1, 'Title': 'Test',
                    'Lanes': [200000012], 'BoardId': 300000000}]
        response = self.app.post('/stations/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_post_stations_with_wrong_lane_id(self):
        payload = [{'Position': 1, 'Title': 'Test',
                    'Lanes': [2000000], 'BoardId': 200000000}]
        response = self.app.post('/stations/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_post_stations_with_duplicate_lanes(self):
        payload = [{'Position': 1, 'Title': 'Test',
                    'Lanes': [200000012, 200000012], 'BoardId': 200000000}]
        response = self.app.post('/stations/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_post_stations_with_inexistent_lane(self):
        payload = [{'Position': 1, 'Title': 'Test',
                    'Lanes': [300000012], 'BoardId': 200000000}]
        response = self.app.post('/stations/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_post_phases_with_inexistent_station(self):
        payload = [{'Position': 0, 'Stations': ['0123456789abcdef01234567'],
                    'Title': 'Test', 'BoardId': 200000000}]
        response = self.app.post('/phases/200000000',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_phases(self):
        response = self.app.get('/phases/100000000')
        self.assertEqual(200, response.status_code)

    def test_phases_not_found(self):
        response = self.app.get('/phases/300000000')
        self.assertEqual(404, response.status_code)

    def test_settings(self):
        response = self.app.get('/settings/100000000')
        self.assertEqual(200, response.status_code)

    def test_settings_not_found(self):
        response = self.app.get('/settings/300000000')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
