from Environment import Environment
from RLAgent import RLAgent
from HumanAgent import  HumanAgent
from RandomAgent import RandomAgent

player1=RLAgent(0.5, 0.5, 0.9, 0.001, 0.01, 1.0)
#player2=HumanAgent("Kashish Narang")
player2=RandomAgent()
Env=Environment(player1,player2,1)

Env.loadFromFile()
Env.playGameAgainstRandomAgent()
Env.resetEnv()
