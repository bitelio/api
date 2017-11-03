from os import path
from json import load, dumps
from pytz import timezone
from datetime import datetime
from pymongo import MongoClient
from tornado.testing import AsyncHTTPTestCase

from api import app


class APITestCase(AsyncHTTPTestCase):
    seed = []

    @classmethod
    def setUpClass(cls):
        for collection in cls.seed:
            db.drop_collection(collection)
            db[collection].insert_many(read(collection))

    @staticmethod
    def get_app():
        return app(debug=False)

    def post(self, url, body):
        return self.fetch(url, method="POST", body=dumps(body or {}))


def read(name):
    folder = path.join(path.dirname(__file__), "data")
    with open(path.join(folder, f"{name}.json")) as json:
        data = load(json)
    if name is "events":
        with open(path.join(folder, "settings.json")) as json:
            settings = load(json)
        timezones = {doc["Id"]: timezone(doc["Timezone"]) for doc in settings}
        for event in data:
            date = datetime.strptime(event["DateTime"], "%Y-%m-%d %H:%M:%S")
            event["DateTime"] = timezones[event["BoardId"]].localize(date)
    return data


db = MongoClient()["test"]
