import openai

from src.server.config.config import Config


class GptClient:
    MODEL = "gpt-3.5-turbo"

    def __init__(self):
        self.agents = Config().active_agents

    def chat(self, message):
        contents = []
        for agent in self.agents:
            messages = [self._format_message(m) for m in agent.memory.get_relevant(message)]
            agent.memory.add(message)
            messages.append(self._format_message(message))
            response = openai.ChatCompletion.create(model=self.MODEL, messages=messages)
            content = response.choices[0].message.content
            agent.memory.add(content)
            contents.append({agent.name: content})
        return contents

    def summarise(self):
        for agent in self.agents:
            question = "Could you summarise our conversation?"
            agent.memory.add(question)
            response = openai.ChatCompletion.create(model=self.MODEL, messages=agent.memory.memories)
            content = response.choices[0].message.content
            agent.memory.clear()
            agent.memory.add(content)

    def _prepare_messages(self, message: str) -> list[dict[str, str]]:
        messages = []
        for agent in self.agents:
            messages.append(self._format_message(agent.goal))
            messages += [self._format_message(m) for m in agent.memory.get_relevant(message)]
            agent.memory.add(message)
            messages.append(self._format_message(message))
        return messages

    def _format_message(self, message: str) -> dict[str, str]:
        return {"role": "user", "content": message}
