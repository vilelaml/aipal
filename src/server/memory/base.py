import abc
from src.server.singleton import AbstractSingleton


class BaseMemorySingleton(AbstractSingleton):
    @abc.abstractmethod
    def add(self, actor, data):
        pass

    @abc.abstractmethod
    def get(self, data):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_relevant(self, data, num_relevant=5):
        pass

    @abc.abstractmethod
    def get_stats(self):
        pass
