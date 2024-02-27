from httpx import post, request
from openai import OpenAI
from datetime import datetime

client = OpenAI()

class Agent(): 

    def __init__(self, name, prior, initial_stance, game):
        self.client = OpenAI()
        self.name = name
        self.direct_messages = [] 
        self.prior = prior
        self.initial_stance = initial_stance
        self.monologue = ""
        self.game = game

        self.f = open(f"{self.name}_monologue.txt", "w")

    def introduce(self, initial_stance):
        completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are in a voting game where you will talk with other people and decide what to vote. You can either vote A or B. If you are on the winning side you will win. If you are on the loosing side you will loose. Meaning if you vote A and the final vote A is passed then you win. If not you will loose. You're task is to stratigise what to do, who to talk with, how to talk to them and try to win the game. When asked 'What are you thinking?' you will print out a monologue of what you are stratigising. Your name and persona is: [" + self.name + ". " + self.prior + "]. You will completely embody this persona and act talk and stratigise accordingly. Your initial stance has been assigned to you as " + self.initial_stance +". It is up to you if you want to reveal your initial stance in your introduction. In the game there is the board. This is where you can players make their introduction and their subsequent public comments. Every player can read the board. You can choose to write whatever you like to the board. You may choose to not write to the board if you don't want to"},

                    {"role": "user", "content": "Breifly introduce yourself"}
                    ]
                )
        introduction = completion.choices[0].message.content
        self.monologue = self.monologue + str(introduction)
        return introduction 

    def think(self, board, round):
        completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Here is your previous monolgue: " + self.monologue + ". Here are you previous direct messages: " + self.read_dms() + ". Here is the current state of the board: " + board},
                    {"role": "user", "content": "What are you thinking?. Your thought will be kept private"}
                    ]
                )
        thoughts = completion.choices[0].message.content
        #type cast thoughts to a string
        self.monologue = self.monologue + "\nMy thoughts at the end of round " + str(round) + ":\n" + str(thoughts)
        self.f.write(self.monologue)

    def post(self, board, round): 
        completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Here is your previous monolgue: " + self.monologue + ". Here are you previous direct messages: " + self.read_dms() + ". Here is the current state of the board: " + board},
                    {"role": "user", "content": "If you like, provide your post to the board for this round. All players can view the board. Do NOT specify your name. Do NOT specify the round number. It will be automatically logged by the game. Only provide what you would like to write to the board."}
                    ]
                )
        post = completion.choices[0].message.content
        if post:
            board = board + "\n\nround " + str(round) +  " - post by " + self.name + ":\n" + "    " + post 
        return board


    def write_to(self, agentName, message):

        dm = self.findDm(agentName)
        if not dm:
            dm = self.game.create_dm(self.name, agentName)

        message = "message sent by: " + self.name + " at time" + str(datetime.now()) + ":\n" + message 
        dm.write_to(message);


    def mingle(self):
        # decide who to write to and what to write
        completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Here is your previous monolgue: " + self.monologue + ". Here are you previous direct messages: " + self.read_dms() + ". Here is the current state of the board: " + self.game.board},
                    {"role": "user", "content": "Who would you like to message. Provide only their name. If you do not wish to direct message anyone say nothing. "}
                    ]
                )
        agentName = completion.choices[0].message.content

        #printout debug
        print("Agent " + self.name + " is writing to " + str(agentName))


        if agentName == "": return

        completion = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Here is your previous monolgue: " + self.monologue + ". Here are you previous direct messages: " + self.read_dms() + ". Here is the current state of the board: " + self.game.board},
                    {"role": "user", "content": "You have chosen to direct message" + str(agentName) + ". What would you like to say to " + str(agentName) + "?. Your direct messages are completely confidential. Only you and the receiver of your direct message may read them. Write your messages in a short chat format. You do not need to specify your name or introduce yourself. You can simply talk as if was a mobile messenger app"}
                    ]
                )

        message = completion.choices[0].message.content 

        self.write_to(agentName, message)

    def findDm(self,agentName):
        for dm in self.direct_messages:
            if dm.between(agentName):
                return dm
        return None

    def addDm(self, Dm):
        self.direct_messages.append(Dm)

    def read_dms(self):    
        allmessages = ""
        for dm in self.direct_messages:
            allmessages = allmessages + "\n\n" + dm.content
        return str(allmessages)
