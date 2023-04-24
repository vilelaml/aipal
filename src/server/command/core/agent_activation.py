from src.server.agent.agent import Agent
from src.server.config.config import Config


class AgentActivation:
    def __init__(self):
        self.config = Config()

    def list_agents(self):
        return Agent.list()

    def activate_agent(self, agent_id):
        self.config.activate_agent(agent_id)

    def deactivate_agent(self, agent_id):
        self.config.deactivate_agent(agent_id)

    def list_active_agents(self):
        return self.config.list_active_agents()
