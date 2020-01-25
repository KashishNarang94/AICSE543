from Environment import Environment
from RLAgent import RLAgent
from RandomAgent import RandomAgent
import matplotlib.pyplot as plt

alpha=[0.1,0.2,0.5,0.7,0.9]
gamma=[0.4,0.5,0.8,0.9,0.99]
epsilon=[0.3,0.7,1]
exploration_decay_rate=0.001
min_epsilon=0.01
max_epsilon=1.0
no_episodes=[1000,2000,3000,4000,5000]

wonRL_alpha=[]

def plot(list2):
    print(alpha)
    print(list2)
    # Plot
    plt.plot(epsilon, list2)
    plt.xlim(0,1)
    plt.ylim(100,2500)
    # naming the x axis
    plt.xlabel('epsilon')
    # naming the y axis
    plt.ylabel('No times RL agent won')
    # function to show the plot
    plt.show()



for i in range(len(epsilon)):
    player1 = RLAgent(alpha[0], gamma[4], epsilon[i], exploration_decay_rate, min_epsilon, max_epsilon)
    player2 = RandomAgent()
    Env = Environment(player1, player2, no_episodes[4])
    wonRL_alpha.append(Env.trainAgent())
    Env.saveIntoFile(i)
plot(wonRL_alpha)


