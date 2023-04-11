import unittest
import json

from src.server.app import app
from src.server.config.config import Config


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        self.config = Config()

    def tearDown(self) -> None:
        del Config._instances[Config]
        del self.config

    def test_list_commands(self):
        self.config.register_command('test', lambda: None)
        self.config.register_command('test_2', lambda: None)
        response = self.client.get('/command')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('commands', data)
        self.assertIsInstance(data['commands'], list)
        self.assertEqual(data['commands'], ['test', 'test_2'])

    def test_process_command(self):
        def show_memories():
            return 'Hello, show_memories!'
        self.config.register_command('show_memories', show_memories)
        response = self.client.post('/command', data={'command': 'show_memories'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertEqual(data['response'], 'Hello, show_memories!')

    def test_process_command_with_args(self):
        def delete_memories(memories):
            return f'Hello, delete_memories: {memories}!'
        self.config.register_command('delete_memories', delete_memories)
        response = self.client.post('/command', data={'command': 'delete_memories', 'args': '{"memories": "all"}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertEqual(data['response'], 'Hello, delete_memories: all!')
