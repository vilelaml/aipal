import unittest
from unittest.mock import patch, MagicMock

from src.server.command.command import Command
from src.server.command.command_exception import CommandNotFoundException
from src.server.config.config import Config


def mytest(text):
    return text


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.commands = {}
        self.config.register_command('exit', exit)

    def test_route(self):
        self.command = Command('exit')
        self.assertEqual(self.command.route(), exit)

    def test_route_custom_function(self):
        self.config.register_command('mytest', mytest)
        self.command = Command('mytest')
        self.assertEqual(self.command.route(), mytest)

    def test_execute(self):
        self.config.register_command('mytest', mytest)
        self.command = Command('mytest', '{"text": "test"}')
        self.assertEqual(self.command.execute(), 'test')

    def test_execute_without_argument(self):
        self.config.register_command('mytest', lambda: 'test')
        self.command = Command('mytest')
        self.assertEqual(self.command.execute(), 'test')

    def test_execute_command_not_found(self):
        self.command = Command('mytest', '{"text": "test"}')
        with self.assertRaises(CommandNotFoundException) as e:
            self.assertEqual(self.command.execute(), 'test')
        self.assertIn("mytest couldn't be loaded. Please verify your configuration", e.exception.args)

