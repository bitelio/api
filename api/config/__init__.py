from os import getenv, path, listdir
from yaml import safe_load


debug = getenv("DEBUG", True)
port = getenv("API_PORT", 8080)
redis = getenv("REDIS_URI", "localhost")
mongo = getenv("MONGODB_URI", "mongodb://localhost/kanban")
dirname = path.dirname(__file__)
for filename in filter(lambda name: name.endswith(".yml"), listdir(dirname)):
    with open(path.join(dirname, filename)) as options:
        locals()[filename[:-4]] = safe_load(options)
