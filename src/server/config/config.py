import importlib

import yaml

from src.server.command.core_commands import CORE_COMMANDS
from src.server.singleton import AbstractSingleton


class Config(AbstractSingleton):
    def __init__(self):
        self.commands = {}

    @property
    def command_names(self):
        return list(self.commands.keys())

    def register_command(self, command, function):
        if command in self.commands:
            raise ValueError(f"{command} is already registered")
        self.commands[command] = function

    def load_core_commands(self):
        for command, action in CORE_COMMANDS.items():
            self.register_command(command, action)

    def load_plugins(self, config_file='aipal.yaml'):
        with open(config_file, "r") as f:
            yaml_data = yaml.safe_load(f)
        base_path = yaml_data['plugin']['base_path']
        for plugin in yaml_data['plugin']['plugins']:
            plugin_path = f"{base_path}/{plugin}/config.yaml"
            self.load_plugin_commands(plugin_path)

    def load_plugin_commands(self, file_path):
        with open(file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
        plugin_module = importlib.import_module(yaml_data["package"])
        plugin_class = yaml_data["class"]
        for command in yaml_data["commands"]:
            plugin_object = getattr(plugin_module, plugin_class)()
            self.register_command(command["name"], getattr(plugin_object, command["function"]))
