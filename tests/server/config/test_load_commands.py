import unittest
from unittest.mock import patch

from src.server.config.config import Config
from src.server.config.load_commands import load_core_commands


class TestLoadCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Config()
        self.config.commands = {}

    def tearDown(self) -> None:
        del Config._instances[Config]
        del self.config

    @patch("src.server.config.load_commands.CORE_COMMANDS", {"test": lambda x: x})
    def test_load_core_commands(self):
        load_core_commands()
        self.assertIn('test', self.config.commands)
