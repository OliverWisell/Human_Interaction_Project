class Agent:
    def __init__(self, name, user):
        self.user = user
        self.name = name
        self.current_result = -1
        self.result = []

    def add_result(self, round_result):
        self.current_result = round_result
        self.result.append(round_result)

    def past_result(self):
        if self.result:
            return self.current_result
        return None
    
    def reset(self):
        self.current_result = -1


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
    def calc_result(self, total):
        if self.total > 0:
            self.result = self.going / total
        else:
            self.result = 0
        self.previous_results.append(self.result)

    #Runs every time a new result should be calculated
    def new_result(self):
        self.going = 0
        total = 0
        for agent in self.agents:
            if agent.past_result() == 1:
                self.going += 1
                total += 1 
            elif agent.past_result() == 0:
                total += 1
        self.total = len(self.agents)
        self.calc_result(total)
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

    def reset_agents(self):
        for agent in self.agents:
            agent.reset()