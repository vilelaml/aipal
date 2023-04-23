from src.server.utils.yaml_datastore import YamlDatastore


class Agent:
    AGENTS_FILE_PATH = 'agents.yaml'
    datastore = YamlDatastore(AGENTS_FILE_PATH)

    def __init__(self, id: int = None, name: str = None, goal: str = None, memory_file: str = None):
        self.id = id
        self.name = name
        self.goal = goal
        self.memory_file = memory_file or name

    @classmethod
    def get(cls, record_id):
        record = cls.datastore.get_record_by_id('Agent', record_id)
        del record["type"]
        return cls(**record)

    def save(self):
        if not hasattr(self, "id") or self.id is None:
            self.id = self.datastore.get_next_id()
        self.datastore.create_record(str(self.id),
                                     {"type": "Agent", "id": self.id, "name": self.name, "goal": self.goal})

    def update(self):
        self.datastore.update_record(str(self.id),
                                     {"type": "Agent", "id": self.id, "name": self.name, "goal": self.goal})

    def delete(self):
        self.datastore.delete_record(str(self.id))

    def __str__(self):
        return f"{self.id} - {self.name}: {self.goal} ({self.memory_file})"
