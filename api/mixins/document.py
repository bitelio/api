from .query import QueryMixin


class DocumentMixin(QueryMixin):
    async def get(self, board_id):
        data = await self.db.find_one(self.query, self.projection)
        self.write(data)
