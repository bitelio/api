from abc import ABCMeta, abstractmethod


class QueryMixin(metaclass=ABCMeta):
    @abstractmethod
    def query(self):
        return NotImplemented

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
