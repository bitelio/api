from .auth import AuthMixin


class BoardMixin(AuthMixin):
    def prepare(self):
        self.board_id = self.path_args["board_id"]
        if self.board_id not in self.user["Boards"]:
            self.write_error(403, "Forbidden")
        else:
            self.log = self.log.bind(board_id=self.board_id)
            super().prepare()

    @property
    def query(self):
        return {"BoardId": self.board_id}
