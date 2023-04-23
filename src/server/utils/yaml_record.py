from src.server.utils.yaml_datastore import YamlDatastore


class YamlRecord:
    BASE_PATH = '.'

    def __init__(self, id: int = None):
        self.id = id
        self.datastore = YamlDatastore(f'{self.BASE_PATH}/{type(self).__name__}.yaml')

    @classmethod
    def get(cls, record_id):
        datastore = YamlDatastore(f'{cls.BASE_PATH}/{cls.__name__}.yaml')
        record = datastore.get_record_by_id(cls.__name__, record_id)
        del record["type"]
        return cls(**record)

    @property
    def __attr__(self) -> dict:
        record = {**{"type": type(self).__name__}, **self.__dict__}
        del record["datastore"]
        return record

    def save(self) -> None:
        self.datastore.reload()
        if not hasattr(self, "id") or self.id is None:
            self.id = self.datastore.get_next_id()
        self.datastore.create_record(str(self.id), self.__attr__)

    def update(self) -> None:
        self.datastore.update_record(str(self.id), self.__attr__)

    def delete(self) -> None:
        self.datastore.delete_record(str(self.id))

