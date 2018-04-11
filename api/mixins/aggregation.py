from .query import QueryMixin


class AggregationMixin(QueryMixin):
    async def get(self, board_id):
        cursor = self.db.aggregate(self.query)
        await cursor.fetch_next
        self.write(cursor.next_object())

    def lookup(self, collection):
        return {
            "$lookup": {
                "from": collection,
                "localField": "Id",
                "foreignField": "BoardId",
                "as": collection.title().replace("_", "")
                }
            }
