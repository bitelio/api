from time import time
from secrets import token_hex
from urllib.error import HTTPError

from api.mixins import PostMixin
from api.models import UserModel, UsernameModel
from api.handlers import BaseHandler


class HelpHandler(PostMixin, BaseHandler):
    model = UsernameModel
    validity = 60 * 60  # seconds
    templates = {
        "activate": "5077e279-b82e-46ea-8034-fdf41d103373",
        "recover": "95851851-5c66-4de4-b12a-8e4a81ccb966"
    }

    async def post(self):
        username = self.body.UserName
        projection = {"_id": 0, "Password": 0}
        query = {"UserName": username, "Password": {"$exists": False}}
        user = await self.mongo.users.find_one(query, projection)
        if user:
            # save token
            query["Password"]["$exists"] = True
            member = await self.mongo.users.find_one(query, projection)
            data = UserModel(member)
            self.log = self.log.bind(user=self.body.UserName)
            deadline = int(time()) + self.validity
            token = token_hex(4) + hex(deadline)[2:]
            data["Token"] = token
            data = {"$set": data.to_native()}
            response = await self.mongo.users.update_one(query, data)
            if response:
                # send email
                link = f"https://bitelio.com/reset/{token}"
                action = "recover" if "Password" in data else "activate"
                name = user["FullName"].capitalize().split()[0]
                email = {
                    "personalizations": [
                        {
                            "to": [{"email": username}],
                            "substitutions": {"-name-": name, "-link-": link}
                        }
                    ],
                    "from": "info@bitelio.com",
                    "template_id": self.templates[action]
                }
                try:
                    self.sg.client.mail.send.post(request_body=email)
                except HTTPError as error:
                    self.write_error(500, error)
                else:
                    self.log = self.log.bind(event="Email sent")
                    self.write({"name": name, "action": action})
            else:
                self.write_error(500, "Error generating token")
        else:
            self.write_error(404, f"Wrong username: {self.body.UserName}")
