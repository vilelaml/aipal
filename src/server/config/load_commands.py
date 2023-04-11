import importlib

import yaml

from src.server.command.core_commands import CORE_COMMANDS
from src.server.config.config import Config


def load_core_commands():
    config = Config()
    for command, action in CORE_COMMANDS.items():
        config.register_command(command, action)


def load_plugin_commands(file_path):
    config = Config()
    with open(file_path, "r") as f:
        yaml_data = yaml.safe_load(f)
    plugin_module = importlib.import_module(yaml_data["package"])
    plugin_class = yaml_data["class"]
    for command in yaml_data["commands"]:
        plugin_object = getattr(plugin_module, plugin_class)()
        config.register_command(command["name"], getattr(plugin_object, command["function"]))
