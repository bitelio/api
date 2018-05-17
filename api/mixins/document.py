from .query import QueryMixin


class DocumentMixin(QueryMixin):
    async def get(self, board_id):
        self.log = self.log.bind(event=f"Reading {self.collection[:-1]}")
        data = await self.db.find_one(self.query, self.projection)
        self.write(data)
