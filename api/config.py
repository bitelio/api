from tornado import options

from api.handlers import NotFoundHandler


def services(module):
    options.db = options.mongo
    return None


db = 
