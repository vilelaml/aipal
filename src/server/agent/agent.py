import yaml


class Agent:
    def __init__(self, agents_file='agents.yaml'):
        self.agents_file = agents_file
        self.agents = []

    def load(self) -> None:
        with open(self.agents_file, 'r') as f:
            self.agents = yaml.safe_load(f)

    def save(self) -> None:
        with open(self.agents_file, 'w') as f:
            yaml.dump(self.agents, f)

    def list(self) -> list[str]:
        return [agent["name"] for agent in self.agents]

    def get(self, name):
        return [d for d in self.agents if d['name'] == name][0]

    def add(self, name, goal) -> None:
        new_agent = {"name": name, "goal": goal}
        self.agents.append(new_agent)

    def delete(self, name) -> bool:
        for idx, agent in enumerate(self.agents):
            if agent['name'] == name:
                self.agents.pop(idx)
                return True
        return False
