import importlib

import yaml

from src.server.agent.agent import Agent
from src.server.singleton import AbstractSingleton
from src.server.memory import *


class Config(AbstractSingleton):
    def __init__(self, config_file='aipal.yaml'):
        self.config_file = config_file
        self.commands = {}
        self.active_agents = []

    @property
    def command_names(self):
        return list(self.commands.keys())

    @property
    def config_yaml(self):
        with open(self.config_file, "r") as f:
            return yaml.safe_load(f)

    @property
    def memory(self):
        memory_class = self.config_yaml['memory']['class']
        memory_file = self.config_yaml['memory']['file_name']
        return globals()[memory_class](memory_file)

    @property
    def agent(self) -> Agent:
        return Agent()

    def initialize(self) -> None:
        self.load_core_commands()
        self.load_plugins()
        self.memory.load()

    def register_command(self, command, function) -> None:
        if command in self.commands:
            raise ValueError(f"{command} is already registered")
        self.commands[command] = function

    def load_core_commands(self) -> None:
        with open('command/core_commands.yaml', "r") as f:
            core_commands = yaml.safe_load(f)

        for ai_client in core_commands['ai_clients']:
            plugin_module = importlib.import_module(ai_client["package"])
            plugin_class = ai_client["class"]
            for command in ai_client["commands"]:
                plugin_object = getattr(plugin_module, plugin_class)()
                self.register_command(command["name"], getattr(plugin_object, command["function"]))

    def load_plugins(self) -> None:
        base_path = self.config_yaml['plugin']['base_path']
        for plugin in self.config_yaml['plugin']['plugins']:
            plugin_path = f"{base_path}/{plugin}/config.yaml"
            self.load_plugin_commands(plugin_path)

    def load_plugin_commands(self, file_path) -> None:
        with open(file_path, "r") as f:
            yaml_data = yaml.safe_load(f)
        plugin_module = importlib.import_module(yaml_data["package"])
        plugin_class = yaml_data["class"]
        for command in yaml_data["commands"]:
            plugin_object = getattr(plugin_module, plugin_class)()
            self.register_command(command["name"], getattr(plugin_object, command["function"]))

    def activate_agent(self, agent_name) -> None:
        self.active_agents.append(self.agent.get(agent_name))

    def deactivate_agent(self, agent_name) -> None:
        for idx, agent in enumerate(self.list_active_agents()):
            if agent == agent_name:
                self.active_agents.pop(idx)

    def list_active_agents(self) -> list[str]:
        return [agent["name"] for agent in self.active_agents]
