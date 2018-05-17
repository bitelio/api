from api.handlers import BaseHandler
from api.mixins import BoardMixin, CollectionMixin


class CardTypesHandler(BoardMixin, CollectionMixin, BaseHandler):
    collection = "card_types"
    response = ["Id", "Name", "ColorHex"]
