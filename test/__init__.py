from os import path, listdir
from json import load, dumps
from pytz import timezone
from datetime import datetime
from tornado.testing import AsyncHTTPTestCase

from api import start


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


def read(collection):
    with open(path.join(folder, f"{collection}.json")) as json:
        data = load(json)
    if collection is "events":
        with open(path.join(folder, "settings.json")) as json:
            settings = load(json)
        timezones = {doc["Id"]: timezone(doc["Timezone"]) for doc in settings}
        for event in data:
            date = datetime.strptime(event["DateTime"], "%Y-%m-%d %H:%M:%S")
            event["DateTime"] = timezones[event["BoardId"]].localize(date)
    return data


folder = path.join(path.dirname(__file__), "data")
collections = [path.basename(filename)[:-5] for filename in listdir(folder)]
