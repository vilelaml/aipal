import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.server.agent.agent import Agent
from src.server.command.core.agent_activation import AgentActivation
from src.server.config.config import Config
from src.server.utils.yaml_datastore import YamlDatastore


class TestAgentActivation(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()
        self.agent_activation = AgentActivation()
        self.temp_dir = TemporaryDirectory()
        self.file_name = f'{self.temp_dir.name}/Agent.yaml'
        datastore = YamlDatastore(self.file_name)
        self.file_patcher = patch.object(Agent, 'BASE_PATH', self.temp_dir.name)
        self.file_patcher.start()

        self.agent1 = Agent(name="Alice", goal="Win the race", memory_class="LocalCache")
        self.agent2 = Agent(name="Bob", goal="Complete the project")
        self.agent1.datastore = datastore
        self.agent2.datastore = datastore
        self.agent1.save()
        self.agent2.save()

    def tearDown(self):
        self.file_patcher.stop()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            self.temp_dir.cleanup()
        del Config._instances[Config]
        del self.config

    def test_list_agents(self):
        expected = {1: 'Alice', 2: 'Bob'}
        result = self.agent_activation.list_agents()
        self.assertEqual(expected, result)

    def test_activate_agent(self):
        expected = self.agent1
        self.agent_activation.activate_agent(1)
        result = self.config.active_agents[0]
        self.assertEqual(expected, result)

    def test_deactivate_agent(self):
        self.config.active_agents.append(self.agent1)
        self.config.active_agents.append(self.agent2)
        expected = self.agent2
        self.agent_activation.deactivate_agent(self.agent1.id)
        result = self.config.active_agents[0]
        self.assertEqual(expected, result)

    def test_list_active_agents(self):
        self.config.active_agents.append(self.agent1)
        expected = {1: 'Alice'}
        result = self.agent_activation.list_active_agents()
        self.assertEqual(expected, result)
