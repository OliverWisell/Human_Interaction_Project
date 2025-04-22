class Agent:
    def __init__(self, name, user):
        self.user = user
        self.name = name
        self.result = []

    def add_result(self, round_result):
        self.result.append(round_result)

    def past_result(self):
        if self.result:
            return self.result[-1]
        return None


class Stats:
    def __init__(self):
        self.agents = []
        self.total = 0
        self.going = 0

        self.result = 0
        self.previous_results = []

    def calc_result(self):
        if self.total > 0:
            self.result = self.going / self.total
        else:
            self.result = 0
        self.previous_results.append(self.result)

    def calculate_result(self):
        self.going = 0
        for agent in self.agents:
            if agent.past_result() == 1:
                self.going += 1
        self.total = len(self.agents)
        self.calc_result()
        return self.result

    def add_agent(self, agent):
        self.agents.append(agent)
        self.total = len(self.agents)

    def find_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def delete_agent(self, name):
        agent_to_remove = self.find_agent(name)
        if agent_to_remove:
            self.agents.remove(agent_to_remove)
            self.total = len(self.agents)
        del agent_to_remove