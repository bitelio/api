from api import route
from api.board import BoardHandler, BoardModel


class UsersModel(BoardModel):
    fields = ["Id", "UserName", "FullName", "Role"]

    @property
    def query(self):
        return self.to_native()


@route
class UsersHandler(BoardHandler):
    async def load(self):
        cursor = self.db.users.find(self.model.query, self.model.projection)
        return await cursor.to_list(None)
