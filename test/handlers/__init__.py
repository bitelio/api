from json import dumps
from tornado.testing import AsyncHTTPTestCase

from api import start
from test import read


class APITestCase(AsyncHTTPTestCase):
    @staticmethod
    def get_app():
        return start("test")

    def tearDown(self):
        self._app.settings["cache"].flushdb()

    def submit(self, method, body):
        return self.fetch(self.url, method=method, body=dumps(body))

    def post(self, body):
        return self.submit("POST", body)

    def put(self, body):
        return self.submit("PUT", body)


def restore(collection):
    def decorate(test):
        def wrapper(self, *args, **kwargs):
            result = test(self, *args, **kwargs)
            db = self._app.settings["db"]
            db.drop_collection(collection)
            db[collection].insert_many(read(collection))
            return result
        return wrapper
    return decorate
