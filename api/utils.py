from re import match
from os import listdir, path
from importlib import import_module


def load(name):
    dirname = path.join(path.dirname(__file__), name)
    module = import_module(f"api.{name}")
    for filename in listdir(dirname):
        if match("[a-z]+.py", filename):
            feature = filename[:-3]
            setattr(module, feature, import_module(f"api.{name}.{feature}"))
    return module
