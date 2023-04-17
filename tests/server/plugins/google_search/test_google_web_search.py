import unittest
from unittest.mock import MagicMock

from src.server.plugins.google_search.google_web_search import GoogleWebSearch


class TestGoogleWebSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.google_client = GoogleWebSearch()

    def test_search(self):
        expected = [
            {"url": "https://example.com", "title": "just an example page"},
            {"url": "https://google.com", "title": "google"},
            {"url": "https://github.com/vilelaml/aipal", "title": "aipal description"},
        ]
        mock_execute = MagicMock()
        mock_execute.return_value = {'items': [
            {'link': 'https://example.com', 'title': 'just an example page'},
            {'link': 'https://google.com', 'title': 'google'},
            {'link': 'https://github.com/vilelaml/aipal', 'title': 'aipal description'}
        ]}
        self.google_client._google_list = MagicMock()
        self.google_client._google_list.execute = mock_execute
        results = self.google_client.search("aipal")
        for idx, result in enumerate(results):
            self.assertDictEqual(result, expected[idx])

    def test__google_list(self):
        mock_list = MagicMock()
        self.google_client.service.cse = MagicMock()
        self.google_client.service.cse().list = mock_list
        self.google_client._google_list('test', 7)
        mock_list.assert_called_once_with(q='test', cx=self.google_client.search_engine_id, num=7)
