import unittest
from unittest import mock
from unittest.mock import patch

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

    @patch("src.server.config.config.CORE_COMMANDS", {"test": lambda x: x})
    def test_load_core_commands(self):
        self.config.load_core_commands()
        self.assertIn('test', self.config.commands)

    def test_load_plugins(self):
        mock_plugin_config = """
        plugin:
          base_path: plugins
          plugins:
            - test_plugin
        """
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_plugin_config)):
            with mock.patch("src.server.config.config.Config.load_plugin_commands") as mock_load_plugin_commands:
                self.config.load_plugins('filepath')
        mock_load_plugin_commands.assert_called_once_with('plugins/test_plugin/config.yaml')

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
            self.config.load_plugin_commands('filepath')
        self.assertIn('confluence_search', self.config.commands)
