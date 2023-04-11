import unittest
from unittest import mock
from unittest.mock import patch

from src.server.config.config import Config
from src.server.config.load_commands import load_core_commands, load_plugin_commands


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

    def test_load_plugin_commands(self):
        mock_plugin_config = """
package: src.server.plugins.confluence.confluence
class: ConfluenceClient
commands:
  - name: confluence_search
    function: confluence_search
    args:
      - search_term
        """
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_plugin_config)):
            load_plugin_commands('filepath')
        self.assertIn('confluence_search', self.config.commands)
