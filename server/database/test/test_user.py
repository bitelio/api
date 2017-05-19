from unittest import TestCase

from .. import user


class User(TestCase):
    def test_get_user_by_email(self):
        data = user.get('user@example.org')
        self.assertDictContainsSubset({'UserName': 'user@example.org'}, data)

    def test_get_user_by_id(self):
        data = user.get(123456789)
        self.assertDictContainsSubset({'Id': 123456789}, data)

    def test_user_not_found(self):
        data = user.get('bogus@example.org')
        self.assertIsNone(data)
