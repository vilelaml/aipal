import unittest

from src.server.config.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()
        self.config.commands = {}
        self.config.register_command('exit', exit)

    def tearDown(self) -> None:
        del Config._instances[Config]
        del self.config

    def test_register_command(self):
        self.assertEqual(self.config.commands['exit'], exit)

    def test_register_command_already_registered(self):
        with self.assertRaises(ValueError) as e:
            self.config.register_command('exit', exit)
        self.assertIn('exit is already registered', e.exception.args)

    def test_command_names(self):
        self.assertEqual(['exit'], self.config.command_names)
