import time


class Controller:

    def __init__(self, qtd_agents, first_conn_time):
        self.connected_agents = {}
        self.agent_job = {}
        self.first_timer = None
        self.step_time = None
        self.terminated = False
        self.simulation_response = None
        self.started = False
        self.qtd_agents = int(qtd_agents)
        self.time_limit = int(first_conn_time)
        self.initial_percepts = None

    def reset_agent_job(self):
        self.agent_job.clear()

    def check_population(self):
        return len(self.connected_agents) < self.qtd_agents

    def check_timer(self):
        return time.time() - self.first_timer < self.time_limit

    def check_agent(self, agent_token):
        return agent_token in self.connected_agents

    def check_connected(self, agent_info):
        for token in self.connected_agents:
            if self.connected_agents[token].agent_info == agent_info:
                return True
        return False

    def check_agents_job(self):
        return len(self.agent_job) == self.qtd_agents

    def dif(self):
        idle_agents = []
        for agent in self.connected_agents:
            if not (agent in self.agent_job):
                idle_agents.append(agent)
        return idle_agents
