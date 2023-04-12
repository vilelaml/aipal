from unittest import TestCase, mock
from unittest.mock import PropertyMock

from atlassian import Confluence

from src.server.plugins.confluence.confluence import ConfluenceClient


class TestConfluenceClient(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.search_term = "test"

        cls.confluence_client = ConfluenceClient()
        cls.confluence_client.confluence_url = 'https://test.atlassian.net/wiki'

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @mock.patch.object(Confluence, "cql")
    def test_confluence_search(self, mock_cql):
        mock_cql.return_value = {
            "results": [{"content": {"id": 1, "title": "test page 1"}}, {"content": {"id": 2, "title": "test page 2"}}]}
        result = self.confluence_client.confluence_search('test')
        self.assertEqual(result, [(1, "test page 1"), (2, "test page 2")])
        mock_cql.assert_called_once_with(f'siteSearch ~ "test"', start=0, limit=10)

    @mock.patch.object(Confluence, "get_page_by_id", return_value={"body": {"storage": {"value": "test page content"}}})
    def test_confluence_read(self, mock_get_page_by_id):
        with mock.patch('src.server.plugins.confluence.confluence.ConfluenceClient.memory',
                        new_callable=PropertyMock()) as mock_memory:
            result = self.confluence_client.confluence_read(page_id=1)
            self.assertEqual(result, "Added page to my knowledge base")
            mock_memory.add.assert_called_once_with("test page content")
            mock_get_page_by_id.assert_called_once_with(1, expand="body.storage")

    @mock.patch.object(ConfluenceClient, "confluence_search")
    @mock.patch.object(ConfluenceClient, "confluence_read")
    def test_search_and_read_first(self, mock_read, mock_search):
        mock_search.return_value = [(1, "test page 1"), (2, "test page 2")]
        mock_read.return_value = "test page content"
        result = self.confluence_client.confluence_search_and_read_first('test')
        self.assertEqual(result, "test page content")
        mock_search.assert_called_once_with(self.search_term)
        mock_read.assert_called_once_with(1)
