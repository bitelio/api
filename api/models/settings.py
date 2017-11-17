from api.models.board import BoardModel


class SettingsModel(BoardModel):
    fields = ["OfficeHours", "Holidays", "Timezone", "Ignore"]

    @property
    def query(self):
        return {"Id": self.BoardId}
