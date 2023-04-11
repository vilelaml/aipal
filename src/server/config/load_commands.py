from src.server.command.core_commands import CORE_COMMANDS
from src.server.config.config import Config


def load_core_commands():
    config = Config()
    for command, action in CORE_COMMANDS.items():
        config.register_command(command, action)
