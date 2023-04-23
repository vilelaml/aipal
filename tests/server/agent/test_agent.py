import os
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch

from src.server.agent.agent import Agent
from src.server.utils.yaml_datastore import YamlDatastore


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.file_name = f'{self.temp_dir.name}/Agent.yaml'
        datastore = YamlDatastore(self.file_name)
        self.file_patcher = patch.object(Agent, 'BASE_PATH', self.temp_dir.name)
        self.file_patcher.start()

        self.agent1 = Agent(name="Alice", goal="Win the race")
        self.agent2 = Agent(name="Bob", goal="Complete the project")
        self.agent1.datastore = datastore
        self.agent2.datastore = datastore

    def tearDown(self):
        self.file_patcher.stop()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            os.rmdir(self.temp_dir.name)

    def test_save(self):
        self.agent1.save()
        self.agent2.save()
        datastore = YamlDatastore(self.file_name)
        self.assertEqual(len(datastore.data), 2)

    def test_get(self):
        self.agent1.save()
        self.agent2.save()
        agent = Agent.get(2)
        self.assertEqual(agent.name, "Bob")
        self.assertEqual(agent.goal, "Complete the project")

    def test_update(self):
        self.agent1.save()
        self.agent1.goal = "Finish the race"
        self.agent1.update()
        agent = Agent.get(1)
        self.assertEqual(agent.goal, "Finish the race")

    def test_delete(self):
        self.agent1.save()
        self.agent2.save()
        self.agent2.delete()
        datastore = YamlDatastore(self.file_name)
        self.assertEqual(len(datastore.data), 1)
        with self.assertRaises(KeyError):
            Agent.get(2)

    def test___str__(self):
        self.agent1.save()
        self.assertEqual("1 - Alice: Win the race (Alice)", self.agent1.__str__())
