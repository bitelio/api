from .query import QueryMixin


class CollectionMixin(QueryMixin):
    async def get(self, board_id):
        cursor = self.db.find(self.query, self.projection)
        self.write(await cursor.to_list(None))
