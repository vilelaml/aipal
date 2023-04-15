from src.server.config.config import Config


class PluginBase:
    @property
    def memory(self):
        return Config().memory
