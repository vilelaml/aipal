import pickle

from src.server.memory.base import BaseMemorySingleton


class LocalMemory(BaseMemorySingleton):
    def __init__(self, file="memory.pkl", autosave=True):
        self.memory_file = file
        self.autosave = autosave
        self.memories = []

    def add(self, actor, data):
        self.memories.append({"role": actor, "content": data})
        if self.autosave:
            self.save()

    def get(self, data):
        return self.get_relevant(data, 1)[0]

    def clear(self):
        self.memory_file = "memory.pkl"
        self.memories = []

    def get_relevant(self, input_str, num_relevant=5):
        return [memory for memory in self.memories if input_str in memory['content']]

    def get_stats(self):
        return len(self.memories)

    def add_user_input(self, data):
        self.add("user", data)

    def save(self):
        with open(self.memory_file, "wb") as f:
            pickle.dump(self.memories, f)

    def load(self):
        with open(self.memory_file, "rb") as f:
            self.memories = pickle.load(f)
