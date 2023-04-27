import os.path
import pickle

from src.server.memory.base import BaseMemorySingleton


class LocalMemory(BaseMemorySingleton):
    def __init__(self, file="memory.pkl", autosave=True):
        self.memory_file = file
        self.autosave = autosave
        self.memories = []

    def add(self, data: str):
        self.memories.append(data)
        if self.autosave:
            self.save()

    def get(self, data):
        return self.get_relevant(data, 1)[0]

    def clear(self):
        self.memories = []
        if self.autosave:
            self.save()

    def get_relevant(self, data: str, num_relevant: int = 5):
        return self.memories[-5:]

    def get_stats(self):
        return len(self.memories)

    def save(self):
        with open(self.memory_file, "wb") as f:
            pickle.dump(self.memories, f)

    def load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "rb") as f:
                try:
                    self.memories = pickle.load(f)
                except EOFError:
                    self.memories = []
