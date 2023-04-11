import unittest
from unittest.mock import patch

from src.server.config.config import Config
from src.server.config.load_commands import load_core_commands


class TestLoadCommands(unittest.TestCase):
    @patch("src.server.config.load_commands.CORE_COMMANDS", {"test": lambda x: x})
    def test_load_core_commands(self):
        load_core_commands()
        config = Config()
        self.assertIn('test', config.commands)
