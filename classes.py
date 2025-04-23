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
        #Agents info
        self.agents = []
        self.total = 0
        self.going = 0

        #Result info
        self.result = 0
        self.previous_results = []

    #Calculates how many went a certain round and adds it to the previous result list.
    def calc_result(self):
        if self.total > 0:
            self.result = self.going / self.total
        else:
            self.result = 0
        self.previous_results.append(self.result)

    #Runs every time a new result should be calculated
    def new_result(self):
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

    def search_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None

    def delete_agent(self, name):
        agent_to_remove = self.search_agent(name)
        if agent_to_remove:
            self.agents.remove(agent_to_remove)
            self.total = len(self.agents)
        del agent_to_remove