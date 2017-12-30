from pytest import fixture
from pymongo import MongoClient

import test


@fixture(scope="session", autouse=True)
def seed():
    client = MongoClient("mongodb://localhost/test")
    client.drop_database("test")
    db = client.get_default_database()
    for collection in test.collections:
        db[collection].insert_many(test.read(collection))
