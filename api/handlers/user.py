from api.mixins import AuthMixin, PostMixin
from api.models import UserModel
from api.handlers import BaseHandler


class UserHandler(AuthMixin, PostMixin, BaseHandler):
    model = UserModel
    roles = {1: "reader", 2: "user", 3: "manager", 4: "administrator"}

    async def get(self):
        self.log = self.log.bind(event=f"Reading user")
        user = {"Boards": []}
        query = [{"$match": {"UserName": self.user["UserName"]}},
                 {"$lookup": {"from": "boards", "localField": "BoardId",
                              "foreignField": "Id", "as": "Board"}},
                 {"$project": {"Password": 0, "_id": 0}}]
        async for item in self.mongo.users.aggregate(query):
            if item["Board"]:
                user["FullName"] = item["FullName"]
                user["GravatarLink"] = item["GravatarLink"]
                user["Boards"].append({"Id": item["BoardId"],
                                       "Title": item["Board"][0]["Title"],
                                       "Enabled": item["Enabled"],
                                       "Role": self.roles[item["Role"]]})
            else:
                user.update(item)
                del user["Board"]
        self.write(user)

    @property
    def query(self):
        return {"UserName": self.user["UserName"]}
