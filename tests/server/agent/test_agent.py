import os
import unittest
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from src.server.agent.agent import Agent
from src.server.utils.yaml_datastore import YamlDatastore


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.temp_file = NamedTemporaryFile(delete=False)
        datastore = YamlDatastore(self.temp_file.name)
        self.ds_patcher = patch.object(Agent, 'datastore', datastore)
        self.ds_patcher.start()

        self.agent1 = Agent(name="Alice", goal="Win the race")
        self.agent2 = Agent(name="Bob", goal="Complete the project")

    def tearDown(self):
        self.ds_patcher.stop()
        self.temp_file.close()
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_save(self):
        self.agent1.save()
        self.agent2.save()
        datastore = YamlDatastore(self.temp_file.name)
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
        datastore = YamlDatastore(self.temp_file.name)
        self.assertEqual(len(datastore.data), 1)
        with self.assertRaises(KeyError):
            Agent.get(2)

    def test___str__(self):
        self.agent1.save()
        self.assertEqual("1 - Alice: Win the race (Alice)", self.agent1.__str__())
