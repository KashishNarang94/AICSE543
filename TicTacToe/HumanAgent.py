class HumanAgent:
    def __init__(self, agentName):
        self.agentName = agentName

    def getName(self):
        return self.agentName

    def chooseAction(self, possible_actions):
        action = int(input("Enter the place you wan to put (1-9) row wise in board "))
        return action-1
