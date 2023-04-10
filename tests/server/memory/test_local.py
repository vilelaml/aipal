import pickle
import unittest
import tempfile
from src.server.memory.local import LocalMemory


class TestLocalMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = LocalMemory(autosave=False)

    def tearDown(self) -> None:
        del LocalMemory._instances[LocalMemory]
        del self.memory

    def test_add_memory(self):
        self.memory.add("user", "this is a test")

        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, self.memory.memories)

    def test_add_memories(self):
        self.memory.add("user", "this is a test")
        self.memory.add("assistant", "ok")

        expected = [
            {"role": "user", "content": "this is a test"},
            {"role": "assistant", "content": "ok"},
        ]
        self.assertEqual(expected, self.memory.memories)

    def test_get(self):
        self.memory.add("user", "this is a test")
        expected_output = {'content': 'this is a test', 'role': 'user'}
        result = self.memory.get("test")
        self.assertDictEqual(expected_output, result)

    def test_clear(self):
        with tempfile.NamedTemporaryFile("wb") as f:
            self.memory.memory_file = f.name

        self.memory.add("user", "this is a test")
        self.memory.clear()

        expected = []
        self.assertEqual(expected, self.memory.memories)
        self.assertEqual("memory.pkl", self.memory.memory_file)

    def test_get_relevant(self):
        self.memory.add("user", "this is a test")
        self.memory.add("user", "this is another test")
        self.memory.add("user", "not this one")
        result = self.memory.get_relevant("test")
        expected_output = [{'content': 'this is a test', 'role': 'user'},
                           {'content': 'this is another test', 'role': 'user'}]
        self.assertEqual(len(expected_output), len(result))
        for i in range(len(expected_output)):
            self.assertDictEqual(expected_output[i], result[i])

    def test_get_stats(self):
        self.memory.add("user", "this is a test")
        self.memory.add("user", "this is another test")
        self.assertEqual(2, self.memory.get_stats())

    def test_save(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            self.memory.memory_file = f.name
            self.memory.add("user", "this is a test")
            self.memory.save()

        with open(self.memory.memory_file, "rb") as f:
            result = pickle.load(f)

        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, result)

    def test_load(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            self.memory.memory_file = f.name
            self.memory.add("user", "this is a test")
            self.memory.save()

        self.memory.load()
        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, self.memory.memories)

    def test_add_user_input(self):
        self.memory.add_user_input("this is a test")

        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, self.memory.memories)


class TestLocalMemoryWithAutosave(unittest.TestCase):
    def setUp(self) -> None:
        self.memory = LocalMemory()

    def tearDown(self) -> None:
        del LocalMemory._instances[LocalMemory]
        del self.memory

    def test_add_memory(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            self.memory.memory_file = f.name
            self.memory.add("user", "this is a test")

        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, self.memory.memories)

        with open(self.memory.memory_file, "rb") as f:
            result = pickle.load(f)

        expected = [{"role": "user", "content": "this is a test"}]
        self.assertEqual(expected, result)
