from schematics.models import Model


class ListModel(Model):
    def __init__(self, raw_data, *args, **kwargs):
        if isinstance(raw_data, list):
            raw_data = {"Body": raw_data}
        super().__init__(raw_data, *args, **kwargs)

    def to_native(self):
        return super().to_native()["Body"]
