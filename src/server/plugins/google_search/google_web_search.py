import os

from src.server.plugins.base import PluginBase
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleWebSearch(PluginBase):
    api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    def __init__(self):
        self.service = build('customsearch', 'v1', developerKey=self.api_key)

    def search(self, query, num_results=10):
        try:
            g_list = self._google_list(query, num_results)
            results = g_list.execute()
            return [{'url': item['link'], 'title': item['title']} for item in results['items']]
        except HttpError as error:
            print('An error occurred: %s' % error)
            return []

    def _google_list(self, query, num):
        return self.service.cse().list(q=query, cx=self.search_engine_id, num=num)
