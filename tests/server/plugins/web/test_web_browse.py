import unittest
from unittest import mock
from unittest.mock import PropertyMock, patch, MagicMock

from src.server.agent.agent import Agent
from src.server.config.config import Config
from src.server.plugins.web.web_browse import WebBrowse


class TestWebBrowse(unittest.TestCase):
    def setUp(self) -> None:
        self.web_browse = WebBrowse()

    def test_is_valid_url_when_valid(self):
        url = 'https://github.com/vilelaml/aipal'
        result = self.web_browse.is_valid_url(url)
        self.assertTrue(result)

    @mock.patch("requests.get")
    def test_read(self, mock_read):
        mock_read.return_value.content = "test page content"
        with mock.patch.object(Agent, 'memory') as mock_agent:
            mock_memory = MagicMock()
            mock_agent.memory = mock_memory
            config = Config()
            config.active_agents = [mock_agent]
            result = self.web_browse.read("https://github.com/vilelaml/aipal")
            self.assertEqual(result, "Added page to my knowledge base")
            mock_memory.add.assert_called_once_with("test page content")
            mock_read.assert_called_once_with("https://github.com/vilelaml/aipal")
