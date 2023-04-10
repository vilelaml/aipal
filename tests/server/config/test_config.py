import unittest

from src.server.config.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()
        self.config.commands = {}

    def test_register_command(self):
        self.config.register_command('exit', exit)
        self.assertEqual(self.config.commands['exit'], exit)

    def test_register_command_already_registered(self):
        self.config.register_command('exit', exit)
        with self.assertRaises(ValueError) as e:
            self.config.register_command('exit', exit)
        self.assertIn('exit is already registered', e.exception.args)
