import sys
import asyncio
import tornado

import api


env = "dev" if sys.argv[-1] == "debug" else "prod"
tornado.platform.asyncio.AsyncIOMainLoop().install()
api.start(env).listen(**tornado.options.options.group_dict("server"))
asyncio.get_event_loop().run_forever()
