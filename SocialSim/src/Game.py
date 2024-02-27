from DirectMessage import DirectMessage
from Agent import Agent

class Game():

    def __init__(self, turns):

        self.agent1 = Agent("John", "You are John, a 24-year-old who thrives on community involvement and social causes. Your day-to-day involves organizing local events, leading volunteer projects, and advocating for community needs. Your approach to the game is grounded in building a sense of camaraderie and consensus among players. You believe that a collective decision, where everyone feels heard and valued, is the key to success. Your initial stance is A, but you're open to discussion and willing to consider other viewpoints if it means reaching a broader agreement.","A",self)

        self.agent2 = Agent("Tracy","You are Tracy, a 34-year-old who runs a popular blog focusing on independent thought and personal empowerment. You're used to analyzing trends, questioning mainstream ideas, and encouraging your readers to think for themselves. In the game, you rely on your ability to critically assess information and persuade others through well-thought-out arguments. Your initial stance is B, but you're always looking for new insights and perspectives that challenge your own views.", "B", self)

        self.agent3 = Agent("Michael", "You are Michael, a 45-year-old high school teacher who loves inspiring young minds. Your days are filled with lessons not just on academic subjects but also on critical thinking, ethics, and the importance of making informed decisions. In the game, you approach each interaction as a teachable moment, guiding discussions with questions that encourage deeper reflection. Your initial stance is A, but your main goal is to ensure that the process is enlightening and enriching for everyone involved.", "A", self)

        self.agents = [self.agent1, self.agent2, self.agent3]
        #store the agents in a hash map, with (name, agent pairs)
        self.agentMap = {} 
        for agent in self.agents:
            self.agentMap[agent.name] = agent
        self.direct_messages = []
        self.turns = turns
        self.board = "THIS IS THE GAME BOARD, EACH PLAYER WILL PRINT THEIR INTRODUCTION AND THEIR INITIAL STANCE HERE AS WELL AS, WHEN THE GAME IS OVER, THEIR FINAL CHOICE A OR B\n\n\n"

        self.board_file = open("board.txt", "w")


    def run(self):

        for agent in self.agents:
            intro = agent.introduce("A")
            self.board = self.board + agent.name + ":\n" + intro + "\n\n"

        print(self.board)

        for i in range(self.turns):
            print("\n\n========== ROUND " + str(i) + " ==========\n\n")
            for agent in self.agents:
                agent.think(self.board, i)

            for i in range(10): # 10 rounds of dms back and fourth
                for agent in self.agents: 
                    agent.mingle() 

            for agent in self.agents:
                self.board = agent.post(self.board, i)

            print("DMs AT THE END OF ROUND " + str(i))
            for dm in self.direct_messages:
                f = open(f"direct_messages_between_{dm.agent1.name}_and_{dm.agent2.name}.txt", "w")
                f.write(dm.content)

            print("BOARD AT THE END OF ROUND " + str(i))
            print(self.board)


    def create_dm(self, agent1Name, agent2Name):

        agent1 = self.agentMap.get(agent1Name) 
        agent2 = self.agentMap.get(agent2Name)

        try:
            if not isinstance(agent1, Agent) or not isinstance(agent2, Agent):
                raise ValueError("One or both specified agents are not instances of the Agent class")
            dm = DirectMessage(agent1,agent2)
            self.direct_messages.append(dm)
            return dm
        except: 
            pass


if __name__ == '__main__':
    game = Game(10)
    game.run()
