class MetaQuery(type):
    def __new__(cls, name, bases, body):
        instance = super().__new__(cls, name, bases, body)
        if "Mixin" not in name:
            for attr in ("collection", "response", "query"):
                if not hasattr(instance, attr):
                    raise TypeError(f"Attribute {attr} missing from {name}")
        return instance


class QueryMixin(metaclass=MetaQuery):
    @property
    def db(self):
        return self.mongo[self.collection]

    @property
    def projection(self):
        keys = {"_id": 0}
        for field in self.response:
            if isinstance(field, str):
                keys[field] = 1
            elif isinstance(field, dict):
                for name, subitems in field.items():
                    for item in subitems:
                        keys[f"{name}.{item}"] = 1
            else:
                raise ValueError("Invalid response format")
        return keys
