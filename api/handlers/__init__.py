from . import auth, base, board


class NotFoundHandler(base.BaseHandler):
    def prepare(self):
        self.write_error(404, "Invalid URL")


def configure(mapper, prefix=""):
    urls = []
    for key, value in mapper.items():
        if isinstance(value, dict):
            urls.extend(configure(value, f"{prefix}/{key}"))
        elif key:
            urls.append((f"{prefix}/{key}", value))
        else:
            urls.append((prefix, value))
    return urls


routes = configure({
    "api": {
        "(?P<board_id>\d{9})": board.routes,
        "auth": auth.routes
    }
})
