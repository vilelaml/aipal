from src.server.utils.yaml_record import YamlRecord


class Agent(YamlRecord):
    def __init__(self, id: int = None, name: str = None, goal: str = None, memory_file: str = None):
        super().__init__(id)
        self.name = name
        self.goal = goal
        self.memory_file = memory_file or name

    def __str__(self) -> str:
        return f"{self.id} - {self.name}: {self.goal} ({self.memory_file})"
