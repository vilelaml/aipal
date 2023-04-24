from src.server.memory import *
from src.server.utils.yaml_record import YamlRecord


class Agent(YamlRecord):
    def __init__(self, id: int = None, name: str = None, goal: str = None, memory_class: str = "LocalMemory",
                 memory_file: str = None):
        super().__init__(id)
        self.name = name
        self.goal = goal
        self.memory_class = memory_class
        self.memory_file = memory_file or name

    @classmethod
    def list(cls) -> dict[int, str]:
        data = super().list()
        return {d["id"]: d["name"] for _, d in data.items()}

    @property
    def memory(self):
        return globals()[self.memory_class](self.memory_file)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}: {self.goal} ({self.memory_file})"

    def __eq__(self, other):
        return self.id == other.id and \
            self.name == other.name and \
            self.goal == other.goal and \
            self.memory_file == other.memory_file
