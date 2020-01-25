import random

#randomplayer player
class RandomAgent:
    def __init__(self):
        pass
    def chooseAction(self,possible_actions):
        action=random.choice(possible_actions)
        return action


