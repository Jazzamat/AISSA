
from Agent import Agent

class DirectMessage():

    def __init__(self, agent1: Agent, agent2: Agent):

        self.title = "Direct Message channel between " + agent1.name + agent2.name

        self.agent1 = agent1
        self.agent2 = agent2

        self.agent1.addDm(self)
        self.agent2.addDm(self)

        self.content = self.title + "\n" 

    def write_to(self, message):
        self.content = self.content + "\n\n" +  message

    def between(self, agentName):
        return (agentName == self.agent1.name) or (agentName == self.agent2.name)

