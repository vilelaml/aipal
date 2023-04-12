import tempfile
import unittest
from unittest import mock
from unittest.mock import patch
import numpy as np
from src.server.memory.local_cache import LocalCache


class TestLocalCache(unittest.TestCase):
    def setUp(self) -> None:
        with tempfile.NamedTemporaryFile("wb") as f:
            self.cache = LocalCache(file=f.name, autosave=False)
        self.cache.load()

    def tearDown(self) -> None:
        del LocalCache._instances[LocalCache]
        del self.cache

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_memories(self):
        self.cache.add("test")
        self.assertEqual(self.cache.memories, ['test'])

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_add(self, _mock_get_ada_embedding):
        self.cache.add("test")
        self.assertEqual(self.cache.data.texts, ['test'])
        self.assertTrue(np.allclose(self.cache.data.embeddings, [1] * 1536))

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_clear(self, _mock_get_ada_embedding):
        self.cache.add("test")
        self.cache.clear()
        self.assertEqual(self.cache.data.texts, [])

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_get(self, _mock_get_ada_embedding):
        self.cache.add("nono")
        self.cache.add("test")
        self.assertEqual(self.cache.get("t"), ["test"])

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_get_relevant(self, _mock_get_ada_embedding):
        self.cache.add("test 1")
        self.cache.add("test 2")
        self.cache.add("test 3")
        self.cache.add("test 4")
        relevant_data = self.cache.get_relevant("test", num_relevant=2)
        self.assertEqual(len(relevant_data), 2)
        self.assertIn("test 4", relevant_data)
        self.assertIn("test 3", relevant_data)

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_get_stats(self, _mock_get_ada_embedding):
        self.cache.add("test 1")
        self.cache.add("test 2")
        length, shape = self.cache.get_stats()
        self.assertEqual(length, 2)
        self.assertEqual(shape, (2, 1536))


class TestLocalCacheSaveAndLoad(unittest.TestCase):
    def setUp(self) -> None:
        if LocalCache in LocalCache._instances:
            del LocalCache._instances[LocalCache]

    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_save(self):
        mock_file = mock.mock_open()
        with mock.patch('builtins.open', mock_file):
            cache = LocalCache(file='test_memory.json', autosave=False)
            cache.load()
            cache.add("this is a test")
            cache.save()
        mock_file.assert_called_once_with('test_memory.json', 'wb')

    def test_load(self):
        mock_memory = '{"texts": ["Hi, another test"], "embeddings": ' + str([1] * 1536) + '}'
        mock_memory = mock_memory.encode('utf-8')
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_memory)):
            with tempfile.NamedTemporaryFile("wb") as f:
                cache = LocalCache(file=f.name, autosave=False)
                cache.load()
        self.assertEqual(cache.data.texts, ["Hi, another test"])

    def test_load_without_file(self):
        with tempfile.NamedTemporaryFile("wb", delete=True) as f:
            file_name = f.name
        cache = LocalCache(file=file_name, autosave=False)
        cache.load()
        self.assertEqual(cache.data.texts, [])

    def test_load_without_content(self):
        mock_memory = b''
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_memory)):
            with tempfile.NamedTemporaryFile("wb") as f:
                cache = LocalCache(file=f.name, autosave=False)
                cache.load()
        self.assertEqual(cache.data.texts, [])


class TestLocalCacheAutoSave(unittest.TestCase):
    @patch('src.server.memory.local_cache.get_ada_embedding', return_value=[1] * 1536)
    def test_add_with_autosave(self, _):
        mock_file = mock.mock_open()
        with mock.patch('builtins.open', mock_file):
            cache = LocalCache(file='test_memory.json', autosave=True)
            cache.load()
            cache.add("test")
        mock_file.assert_called_once_with('test_memory.json', 'wb')

