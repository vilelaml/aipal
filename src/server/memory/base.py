import abc
import openai
import yaml

from src.server.singleton import AbstractSingleton


def get_ada_embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]


class BaseMemorySingleton(AbstractSingleton):
    @abc.abstractmethod
    def add(self, data: str):
        pass

    @abc.abstractmethod
    def get(self, data: str):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_relevant(self, data: str, num_relevant: int = 5):
        pass

    @abc.abstractmethod
    def get_stats(self):
        pass
