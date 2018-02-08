from api import route
from api.board import BoardHandler, BaseBoardModel


class UsersModel(BaseBoardModel):
    fields = ["Id", "UserName", "FullName", "Role"]


@route
class UsersHandler(BoardHandler):
    async def load(self):
        cursor = self.db.users.find(self.model.query, self.model.projection)
        return await cursor.to_list(None)
