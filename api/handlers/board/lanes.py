from api.handlers import BaseHandler
from api.mixins import BoardMixin, CollectionMixin


class LanesHandler(BoardMixin, CollectionMixin, BaseHandler):
    collection = "lanes"
    response = ["Id", "Title", "Top", "Width", "Height", "Left",
                "ChildLaneIds"]
