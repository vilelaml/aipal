import unittest
from unittest import mock

from src.server.agent.agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self) -> None:
        mock_agent_config = """
                - name: test
                  goal: be the first test
                - name: test2
                  goal: be the second test
                """
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_agent_config)):
            self.agent = Agent()
            self.agent.load()

    def test_list_agents(self):
        expected = ['test', 'test2']
        result = self.agent.list()
        self.assertEqual(expected, result)

    def test_get_agent(self):
        expected = {"name": "test", "goal": "be the first test"}
        result = self.agent.get("test")
        self.assertEqual(expected, result)

    def test_add_agent(self):
        self.agent.add(name="test3", goal="third agent")
        expected = ['test', 'test2', 'test3']
        result = self.agent.list()
        self.assertEqual(expected, result)

    def test_delete_agent(self):
        result = self.agent.delete(name="test2")
        expected = ['test']
        agents = self.agent.list()
        self.assertTrue(result)
        self.assertEqual(expected, agents)

    def test_delete_agent_not_found(self):
        result = self.agent.delete(name="not_found")
        expected = ['test', 'test2']
        agents = self.agent.list()
        self.assertFalse(result)
        self.assertEqual(expected, agents)
