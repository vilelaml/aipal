import unittest
from unittest import mock
from unittest.mock import PropertyMock, patch

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
        with mock.patch("src.server.plugins.web.web_browse.WebBrowse.memory",
                        new_callable=PropertyMock()) as mock_memory:
            result = self.web_browse.read("https://github.com/vilelaml/aipal")
            self.assertEqual(result, "Added page to my knowledge base")
            mock_memory.add.assert_called_once_with("test page content")
            mock_read.assert_called_once_with("https://github.com/vilelaml/aipal")
