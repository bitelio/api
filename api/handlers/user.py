from api import route
from api.handlers import BaseHandler


@route
class UserHandler(BaseHandler):
    roles = {1: "reader", 2: "user", 3: "manager", 4: "administrator"}

    async def post(self):
        boards = []
        async for document in self.db.users.aggregate(self.model.query):
            boards.append({"BoardId": document["BoardId"],
                           "BoardTitle": document["Board"][0]["Title"],
                           "Enabled": document["Enabled"],
                           "Role": self.roles[document["Role"]]})
        if boards:
            fields = ["Id", "FullName", "UserName"]
            user = {key: document[key] for key in fields}
            user["Boards"] = boards
            self.write(user)
        else:
            self.write_error(404, f"User {self.model.UserName} not found")
