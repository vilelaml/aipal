import unittest
import json
from src.server.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

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
        self.assertEqual(data['message'], 'Hello, adelete_memories!')
