from src.server.language_model.gpt_client import GptClient

CORE_COMMANDS = {
    "chat": GptClient().chat
}
