import json

from src.server.command.command_exception import CommandNotFoundException
from src.server.config.config import Config


class Command:
    def __init__(self, command, args="{}"):
        self.command = command
        self.args = json.loads(args)
        self.config = Config()

    def route(self):
        if self.command not in self.config.commands:
            raise CommandNotFoundException(f"{self.command} couldn't be loaded. Please verify your configuration")
        return self.config.commands[self.command]

    def execute(self):
        command = self.route()
        return command(**self.args)

