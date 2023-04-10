import unittest
from src.server.memory.base import BaseMemorySingleton


class TestBaseMemorySingleton(unittest.TestCase):
    def test_has_add_method(self):
        self.assertTrue(hasattr(BaseMemorySingleton, 'add'))

    def test_has_get_method(self):
        self.assertTrue(hasattr(BaseMemorySingleton, 'get'))

    def test_has_clear_method(self):
        self.assertTrue(hasattr(BaseMemorySingleton, 'clear'))

    def test_has_get_relevant_method(self):
        self.assertTrue(hasattr(BaseMemorySingleton, 'get_relevant'))

    def test_has_get_stats_method(self):
        self.assertTrue(hasattr(BaseMemorySingleton, 'get_stats'))
