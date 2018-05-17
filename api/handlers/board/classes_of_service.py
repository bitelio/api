from api.handlers import BaseHandler
from api.mixins import BoardMixin, CollectionMixin


class ClassesOfServiceHandler(BoardMixin, CollectionMixin, BaseHandler):
    collection = "classes_of_service"
    response = ["Id", "Title"]
