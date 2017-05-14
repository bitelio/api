import pymongo

from .. import config


client = pymongo.MongoClient(config.mongodb_uri)
db = client.get_default_database()
