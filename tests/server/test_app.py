import unittest
import json
from unittest.mock import patch

from src.server.app import app
from src.server.language_model.gpt_client import GptClient


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch.object(GptClient, 'chat')
    def test_chat(self, mock_chat):
        mock_chat.return_value = "Hello, how can I assist you?"
        response = self.client.post('/chat', data={'message': 'Hi there!'})
        data = response.get_json()

        mock_chat.assert_called_once_with('Hi there!')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['response'], "Hello, how can I assist you?")

    def test_list_commands(self):
        response = self.client.get('/command')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('commands', data)
        self.assertIsInstance(data['commands'], list)
        self.assertEqual(data['commands'], ['show_memories'])

    def test_process_command(self):
        response = self.client.post('/command', data={'command': 'show_memories'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Hello, show_memories!')

    def test_process_command_with_args(self):
        response = self.client.post('/command', data={'command': 'delete_memories', 'args': 'all'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Hello, delete_memories!')
