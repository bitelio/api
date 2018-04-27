from copy import deepcopy
from api.handlers import BaseHandler
from api.models import StationsModel
from api.mixins import BoardMixin, PostMixin, CollectionMixin


class StationsHandler(BoardMixin, PostMixin, CollectionMixin, BaseHandler):
    collection = "stations"
    model = StationsModel
    response = ["Name", "Card", "Size", "Lanes", "Phase"]

    async def post(self, board_id):
        body = self.body.to_native()
        await self.db.remove(self.query)
        await self.db.insert_many(deepcopy(body))
        self.write(body)
