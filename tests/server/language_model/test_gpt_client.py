import os
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest.mock import MagicMock, patch
import openai

from src.server.agent.agent import Agent
from src.server.language_model.gpt_client import GptClient
from src.server.utils.yaml_datastore import YamlDatastore


class TestGptClient(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.file_name = f'{self.temp_dir.name}/Agent.yaml'
        datastore = YamlDatastore(self.file_name)
        self.file_patcher = patch.object(Agent, 'BASE_PATH', self.temp_dir.name)
        self.file_patcher.start()
        self.client = GptClient()
        self.memory_file = NamedTemporaryFile(delete=False).name
        self.agent1 = Agent(name="test", goal="Run a test", memory_file=self.memory_file)
        self.agent1.datastore = datastore
        self.client.agents = [self.agent1]

    def tearDown(self) -> None:
        self.file_patcher.stop()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            self.temp_dir.cleanup()
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)

    @patch.object(openai.ChatCompletion, 'create')
    def test_chat(self, mock_create):
        message = "Hello, how are you?"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="I'm good, thanks!"))]
        mock_create.return_value = mock_response

        result = self.client.chat(message)

        full_message = {'role': 'user', 'content': message}
        mock_create.assert_called_once_with(model=self.client.MODEL, messages=[full_message])
        expected = [{'test': "I'm good, thanks!"}]
        self.assertEqual(expected, result)

    @patch.object(openai.ChatCompletion, 'create')
    def test_summarise(self, mock_create):
        messages = ['Could you summarise our conversation?']
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="We talked about various topics."))]
        mock_create.return_value = mock_response

        self.client.summarise()

        mock_create.assert_called_once_with(model=self.client.MODEL, messages=messages)
        self.assertEqual(len(self.agent1.memory.memories), 1)
        self.assertEqual(self.agent1.memory.get(""), 'We talked about various topics.')

    def test__prepare_messages(self):
        self.agent1.memory.add("Memory 1")
        self.agent1.memory.add("Memory 2")
        expected = [{"role": "user", "content": "Run a test"},
                    {"role": "user", "content": "Memory 1"},
                    {"role": "user", "content": "Memory 2"},
                    {"role": "user", "content": "message"}]
        result = self.client._prepare_messages("message")
        self.assertEqual(expected, result)
