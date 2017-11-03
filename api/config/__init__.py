from yaml import safe_load
from os import listdir, path


dirname = path.dirname(__file__)
for filename in filter(lambda name: name.endswith(".yml"), listdir(dirname)):
    with open(path.join(dirname, filename)) as options:
        locals()[filename[:-4]] = safe_load(options)
