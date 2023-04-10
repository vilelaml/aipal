from src.server.singleton import AbstractSingleton


class Config(AbstractSingleton):
    def __init__(self):
        self.commands = {}

    def register_command(self, command, function):
        if command in self.commands:
            raise ValueError(f"{command} is already registered")
        self.commands[command] = function
