from api.mixins import AuthMixin, PostMixin
from api.models import UserModel
from api.handlers import BaseHandler


class UserHandler(AuthMixin, PostMixin, BaseHandler):
    model = UserModel
    collection = "accounts"
    roles = {1: "reader", 2: "user", 3: "manager", 4: "administrator"}

    async def get(self):
        self.log = self.log.bind(event=f"Reading user")
        projection = {"Token": 0, "Password": 0, "_id": 0}
        query = {"UserName": self.user["UserName"]}
        user = await self.mongo.accounts.find_one(query, projection)
        query = [{"$match": {"UserName": self.user["UserName"]}},
                 {"$lookup": {"from": "boards", "localField": "BoardId",
                              "foreignField": "Id", "as": "Board"}}]
        cursor = self.mongo.users.aggregate(query)
        items = await cursor.to_list(None)
        user["Boards"] = [{"Id": item["BoardId"],
                           "Title": item["Board"][0]["Title"],
                           "Enabled": item["Enabled"],
                           "Role": self.roles[item["Role"]]}
                          for item in items]
        extra = ["Id", "FullName", "GravatarLink"]
        user.update(**{key: items[0][key] for key in extra})
        self.write(user)

    async def delete(self):
        self.log = self.log.bind(event=f"Deleting user")
        username = self.user["UserName"]
        response = await self.mongo.accounts.delete_one({"UserName": username})
        if response.deleted_count == 1:
            token = self.get_cookie("token")
            self.redis.delete(f"session:{token}")
            self.write({"message": "User deleted"})
        else:
            self.write_error(500, "Couldn't delete user")

    @property
    def query(self):
        return {"UserName": self.user["UserName"]}
