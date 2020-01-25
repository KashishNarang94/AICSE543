import pickle
import random
import numpy as np
import itertools


class RLAgent:

    def __init__(self, alpha, gamma, epsilon, exploration_decay_rate, min_epsilon, max_epsilon):
        # Qlearning parameters
        self.alpha = alpha
        self.gamma = gamma

        # Greedy policy parameters
        self.epsilon = epsilon
        self.exploration_decay_rate = exploration_decay_rate
        self.min_epsilon = min_epsilon
        self.max_epsilon = max_epsilon

        # Q table : a dictionary key = state/board in string format and value= action for 0 to 9
        self.Q = dict()

    def chooseAction(self, curr_board,possible_actions):
        exploration_rate = random.uniform(0, 1)

        # Get all actions
        actions = possible_actions
        curr_board_str=str(curr_board)
        if exploration_rate > self.epsilon:  # Exploit

            if curr_board_str in self.Q:
                qvalues = np.array(self.Q[curr_board_str])
                possible_action_qvalues = qvalues[actions]
                best_qvalue = np.max(possible_action_qvalues)
                action_to_be = list(self.Q[curr_board_str]).index(best_qvalue)

            else:
                # State not available in QTable, so add it but choose any random available action
                self.Q[curr_board_str] = [0 for i in range(9)]
                action_to_be = random.choice(actions)

        else:  # Explore
            self.Q[curr_board_str] = [0 for i in range(9)]
            action_to_be = random.choice(actions)

        return action_to_be


    def addNewBoardtoQtable(self,new_board):
        new_board_str = str(new_board)
        if new_board_str not in self.Q:
            self.Q[new_board_str] = [0 for i in range(9)]

    def epsilon_decay(self,episode_no):
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.exploration_decay_rate * episode_no)
        print("New epsilon is : ", self.epsilon)

    def updateQtable(self, curr_board, new_board, action, reward ):
        new_board_str = str(new_board)
        curr_board_str = str(curr_board)
        mdp = self.alpha * (reward + self.gamma * (np.max(self.Q[new_board_str]) - self.Q[curr_board_str][action]))
        self.Q[curr_board_str][action] = self.Q[curr_board_str][action] + mdp;

    def storeQvalue(self, file):
        with open(file, 'wb') as handle:
            pickle.dump(self.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQvalue(self, file):
        with open(file, 'rb') as handle:
            self.Q = pickle.load(handle)
