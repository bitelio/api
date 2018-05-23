from api.handlers import BaseHandler
from api.models import StationsModel
from api.mixins import BoardMixin, PostMixin, CollectionMixin


class StationsHandler(BoardMixin, PostMixin, CollectionMixin, BaseHandler):
    collection = "stations"
    model = StationsModel
    response = ["Name", "Card", "Size", "Lanes", "Phase"]

    async def post(self, *args, **kwargs):
        body = self.body.to_native()
        stations = [dict(BoardId=self.board_id, **s) for s in body]
        await self.db.remove(self.query)
        await self.db.insert_many(stations)
        self.write(body)
