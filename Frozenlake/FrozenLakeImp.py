import pickle

import numpy as np
import random
import time
import gym
import matplotlib.pyplot as plt

#Make Environment of Frozen Lake
environment=gym.make("FrozenLake-v0")

#Create and Initialize Q table with all zeroes
no_states=environment.observation_space.n
print(no_states)
no_actions=environment.action_space.n
print(no_actions)
q_table=np.zeros([no_states,no_actions])
print(q_table)

#Q Learning parameters
max_episodes=10000
max_steps_per_episode=100
alpha=0.1
gamma=0.9


#Greedy policy parameters
epsilon=0.5
exploration_decay_rate=0.002
min_epsilon=0.01
max_epsilon=1.0

rewards_per_episode = []
steps_per_episode=[]
time_per_episode=[]


def selectAction(curr_state):
    exploration_rate = random.uniform(0, 1)
    if exploration_rate > epsilon:
        action_to_be = np.argmax(q_table[curr_state, :])
    else:
        action_to_be = environment.action_space.sample()
    return action_to_be


for i in range(max_episodes):
    ep_start_time=time.time()
    curr_state=environment.reset()
    done=False
    total_reward=0
    total_steps=0
    total_time=0

    for j in range(max_steps_per_episode):

        # E-greedy
        action_to_be = selectAction(curr_state)
        print(action_to_be)

        # Take new action
        new_state, reward, done, info = environment.step(action_to_be)

        # Update Q-table
        MDP=alpha*(reward+gamma*np.max(q_table[new_state,:])-q_table[curr_state,action_to_be])
        q_table[curr_state,action_to_be]=q_table[curr_state,action_to_be]+MDP;

        # Set new state
        curr_state=new_state

        # Add new reward and steps taken
        total_reward+=reward
        total_steps=j

        #Break condition if agent reached Hole or End state
        environment.render()
        if done:
            break

    # Exploration rate decay
    epsilon=min_epsilon + (max_epsilon- min_epsilon) * np.exp(-exploration_decay_rate*i)
    print("New epsilon is : ",epsilon)

    # Add current episode reward to total rewards list
    rewards_per_episode.append(total_reward)

    #Add current episodes steps taken
    steps_per_episode.append(total_steps)

    print("Episode Completed :",i)
    total_time=time.time()-ep_start_time
    time_per_episode.append(round(total_time,5))

#print(rewards_per_episode)
#print(steps_per_episode)
#print(time_per_episode)

#How many times reached goal
count_goal_reach=0
for i in rewards_per_episode:
    if i==1.0:
        count_goal_reach+=1
print("Reached goal in total ",count_goal_reach," times")


#Average reward per 1000 epidodes
list1=[]
list2=[]
list3=[]
rewards_per_thosand= np.split(np.array(rewards_per_episode),max_episodes/1000)
count = 1000
print("\n********Average reward per thousand episodes********\n")
for i in rewards_per_thosand:
    #print(count, ": ", str(sum(i/1000)))
    list1.append(count)
    list2.append(sum(i/1000))
    count += 1000

print(list1)
print(list2)



plt.plot(list1, list2)
plt.xlim(0, 11000)
plt.ylim(0, 0.8)
# naming the x axis
plt.xlabel('Episodes')
# naming the y axis
plt.ylabel('Avg No times RL agent won')
# function to show the plot
plt.show()













"""
def play():
    for i in range(100):             #episodes
        ep_start_time = time.time()
        curr_state = environment.reset()
        done = False
        total_reward = 0
        total_steps = 0
        total_time = 0

        for j in range(100):        #max_steps
            action_to_be = selectAction(curr_state)
            print(action_to_be)
            new_state, reward, done, info = environment.step(action_to_be)
            curr_state = new_state

            # Add new reward and steps taken
            total_reward += reward
            total_steps = j

            # Break condition if agent reached Hole or End state
            environment.render()
            if done:
                break

        # Add current episode reward to total rewards list
        rewards_per_episode.append(total_reward)

        # Add current episodes steps taken
        steps_per_episode.append(total_steps)

        print("Episode Completed :", i)
        total_time = time.time() - ep_start_time
        time_per_episode.append(round(total_time, 5))

    print(rewards_per_episode)
    print(steps_per_episode)
    print(time_per_episode)
    count_goal_reach = 0
    for i in rewards_per_episode:
        if i == 1.0:
            count_goal_reach += 1
    print("Reached goal ", count_goal_reach, " times")

play()

"""
