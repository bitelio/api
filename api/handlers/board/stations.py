from copy import deepcopy
from api.handlers import BaseHandler
from api.mixins import BoardMixin, CollectionMixin, EditableMixin


class StationsHandler(BoardMixin, CollectionMixin, EditableMixin, BaseHandler):
    collection = "stations"
    response = ["Name", "Card", "Size", "Lanes", "Phase"]

    async def post(self, board_id):
        await self.db.remove(self.query)
        await self.db.insert_many(deepcopy(self.payload))
        self.write(self.payload)
