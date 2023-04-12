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
        self.memory.add("this is a test")

        expected = ["this is a test"]
        self.assertEqual(expected, self.memory.memories)

    def test_add_memories(self):
        self.memory.add("this is a test")
        self.memory.add("ok")

        expected = ["this is a test", "ok"]
        self.assertEqual(expected, self.memory.memories)

    def test_get(self):
        self.memory.add("this is a test")
        expected_output = 'this is a test'
        result = self.memory.get("test")
        self.assertEqual(expected_output, result)

    def test_clear(self):
        with tempfile.NamedTemporaryFile("wb") as f:
            self.memory.memory_file = f.name

        self.memory.add("this is a test")
        self.memory.clear()

        expected = []
        self.assertEqual(expected, self.memory.memories)
        self.assertEqual("memory.pkl", self.memory.memory_file)

    def test_get_relevant(self):
        self.memory.add("this is a test")
        self.memory.add("this is another test")
        self.memory.add("not this one")
        result = self.memory.get_relevant("test")
        expected_output = ['this is a test', 'this is another test']
        self.assertEqual(len(expected_output), len(result))
        for i in range(len(expected_output)):
            self.assertEqual(expected_output[i], result[i])

    def test_get_stats(self):
        self.memory.add("this is a test")
        self.memory.add("this is another test")
        self.assertEqual(2, self.memory.get_stats())

    def test_save(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            self.memory.memory_file = f.name
            self.memory.add("this is a test")
            self.memory.save()

        with open(self.memory.memory_file, "rb") as f:
            result = pickle.load(f)

        expected = ["this is a test"]
        self.assertEqual(expected, result)

    def test_load(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            self.memory.memory_file = f.name
            self.memory.add("this is a test")
            self.memory.save()

        self.memory.load()
        expected = ["this is a test"]
        self.assertEqual(expected, self.memory.memories)

    def test_load_when_file_doesnt_exist(self):
        with tempfile.NamedTemporaryFile("wb", delete=True) as f:
            self.memory.memory_file = f.name
        self.memory.load()
        expected = []
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
            self.memory.add("this is a test")

        expected = ["this is a test"]
        self.assertEqual(expected, self.memory.memories)

        with open(self.memory.memory_file, "rb") as f:
            result = pickle.load(f)

        expected = ["this is a test"]
        self.assertEqual(expected, result)
