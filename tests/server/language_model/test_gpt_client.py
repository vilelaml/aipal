import unittest
from unittest.mock import MagicMock, patch
import openai
from src.server.memory.local import LocalMemory
from src.server.language_model.gpt_client import GptClient


class TestGptClient(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = LocalMemory(autosave=False)
        self.client = GptClient()

    def tearDown(self) -> None:
        del LocalMemory._instances[LocalMemory]
        del self.memory

    @patch.object(openai.ChatCompletion, 'create')
    def test_chat(self, mock_create):
        message = "Hello, how are you?"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="I'm good, thanks!"))]
        mock_create.return_value = mock_response

        result = self.client.chat(message)

        mock_create.assert_called_once_with(model=self.client.MODEL, messages=self.client.memory.memories)
        self.assertEqual(result, "I'm good, thanks!")
        self.assertDictEqual(self.client.memory.get("good"), {'role': 'assistant', 'content': "I'm good, thanks!"})

    @patch.object(openai.ChatCompletion, 'create')
    def test_summarise(self, mock_create):
        messages = [{'role': 'user', 'content': 'Could you summarise our conversation?'}]
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="We talked about various topics."))]
        mock_create.return_value = mock_response

        self.client.summarise()

        mock_create.assert_called_once_with(model=self.client.MODEL, messages=messages)
        self.assertEqual(len(self.client.memory.memories), 1)
        self.assertDictEqual(self.client.memory.get(""), {'role': 'assistant', 'content': 'We talked about various topics.'})
