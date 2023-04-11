import os
from atlassian import Confluence

from src.server.memory.local import LocalMemory


class ConfluenceClient:
    api_token = os.getenv("ATLASSIAN_API_KEY")
    confluence_url = os.getenv("CONFLUENCE_URL")
    username = os.getenv("ATLASSIAN_USERNAME")

    @property
    def memory(self):
        return LocalMemory()

    @property
    def client(self):
        return Confluence(url=self.confluence_url, username=self.username, password=self.api_token)

    def confluence_search(self, search_term):
        cql_query = f'siteSearch ~ "{search_term}"'
        pages = self.client.cql(cql_query, start=0, limit=10)
        return [(page['content']['id'], page['content']['title']) for page in pages['results']]

    def confluence_read(self, page_id):
        page_content = self.client.get_page_by_id(page_id, expand="body.storage")["body"]["storage"]["value"]
        self.memory.add_user_input(page_content)
        return 'Added page to my knowledge base'

    def confluence_search_and_read_first(self, search_term):
        pages = self.confluence_search(search_term)
        return self.confluence_read(pages[0][0])
