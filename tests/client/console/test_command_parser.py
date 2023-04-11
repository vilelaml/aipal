import unittest

from src.client.console.aipal_client import command_parser


class TestCommandParser(unittest.TestCase):
    def test_command_without_argument(self):
        result = command_parser("/call")
        self.assertDictEqual({"command": "call", "args": '{}'}, result)

    def test_command_with_argument(self):
        result = command_parser("/call page=me id=1")
        self.assertDictEqual({"command": "call", "args": '{"page": "me", "id": "1"}'}, result)

    def test_chat(self):
        result = command_parser("Anything really")
        self.assertDictEqual({"command": "chat", "args": '{"message": "Anything really"}'}, result)
