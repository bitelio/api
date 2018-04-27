from os import path, listdir
from json import load, dumps
from pytz import timezone
from datetime import datetime
from tornado.testing import AsyncHTTPTestCase

from api import start


class BaseTestCase(AsyncHTTPTestCase):
    @staticmethod
    def get_app():
        app = start("test")
        cookie = '{"UserName": "user@example.org", "Boards": {"100000000": 4}}'
        app.settings["redis"].set("session:xxx", cookie)
        return app

    def get(self, url=None, **kwargs):
        return self.fetch(url or self.url, **kwargs)

    def post(self, body):
        return self.get(self.url, method="POST", body=dumps(body))


def restore(collection):
    def decorate(test):
        def wrapper(self, *args, **kwargs):
            result = test(self, *args, **kwargs)
            mongo = self._app.settings["mongo"]
            mongo.drop_collection(collection)
            mongo[collection].insert_many(read(collection))
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
