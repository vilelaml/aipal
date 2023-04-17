import requests
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from src.server.plugins.base import PluginBase


class WebBrowse(PluginBase):
    def is_valid_url(self, url) -> bool:
        result = urlparse(url)
        return all([result.scheme, result.netloc])

    def read(self, url):
        if self.is_valid_url(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.memory.add(soup.get_text())
            return 'Added page to my knowledge base'
