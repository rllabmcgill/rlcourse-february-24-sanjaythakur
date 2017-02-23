
# coding: utf-8

# In[1]:

import random


# All constants

# In[2]:

#Discount-factor
GAMMA = 0.95

#ALPHA or step-size
ALPHA = 0.1

#Defining the EPSILON which would ensure regular exploration. Our EPSILON will decrease linearly with each iteration of a episode and will eventually fade away to 0 .
EPSILON = 1

#Number of episodes to consider
TOTAL_EPISODES_TO_CONSIDER = 1000

#Maximum allowed episode length
MAXIMUM_EPISODE_LENGTH = 100

#Number of planning steps
NUMBER_PLANNING_STEPS = 50

#All possible actions defined
ACTION_UP = 'UP'
ACTION_DOWN = 'DOWN'
ACTION_LEFT = 'LEFT'
ACTION_RIGHT = 'RIGHT'

#Start and end of any episode
START_STATE = '00'
END_STATE = '15'


# Defining the MDP

# In[3]:

all_states = ['00', '01', '02', '03',
          '04', '05', '06', '07',
          '08', '09', '10', '11',
          '12', '13', '14', '15']


# Parameters to mimic the environment. Remember that these parameters won't be known to us, not at least before we start moving our agent.

# In[4]:

immediate_state_rewards =  {
    '00': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '01': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '02': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '03': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '04': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '05': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '06': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '07': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '08': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '09': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '10': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '11': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '12': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '13': {ACTION_UP : 0, ACTION_RIGHT : 0, ACTION_DOWN: 1, ACTION_LEFT: 0},
    '14': {ACTION_UP : 0, ACTION_RIGHT : 1, ACTION_DOWN: 0, ACTION_LEFT: 0},
    '15': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
}

all_transitions =  {
    '00': {ACTION_UP : '00', ACTION_RIGHT : '01', ACTION_DOWN: '04', ACTION_LEFT: '00'},
    '01': {ACTION_UP : '01', ACTION_RIGHT : '02', ACTION_DOWN: '05', ACTION_LEFT: '00'},
    '02': {ACTION_UP : '02', ACTION_RIGHT : '03', ACTION_DOWN: '06', ACTION_LEFT: '01'},
    '03': {ACTION_UP : '03', ACTION_RIGHT : '03', ACTION_DOWN: '07', ACTION_LEFT: '02'},
    '04': {ACTION_UP : '00', ACTION_RIGHT : '05', ACTION_DOWN: '08', ACTION_LEFT: '04'},
    '05': {ACTION_UP : '01', ACTION_RIGHT : '06', ACTION_DOWN: '09', ACTION_LEFT: '04'},
    '06': {ACTION_UP : '02', ACTION_RIGHT : '07', ACTION_DOWN: '10', ACTION_LEFT: '05'},
    '07': {ACTION_UP : '03', ACTION_RIGHT : '07', ACTION_DOWN: '11', ACTION_LEFT: '06'},
    '08': {ACTION_UP : '04', ACTION_RIGHT : '09', ACTION_DOWN: '12', ACTION_LEFT: '08'},
    '09': {ACTION_UP : '05', ACTION_RIGHT : '10', ACTION_DOWN: '13', ACTION_LEFT: '08'},
    '10': {ACTION_UP : '06', ACTION_RIGHT : '11', ACTION_DOWN: '14', ACTION_LEFT: '09'},
    '11': {ACTION_UP : '07', ACTION_RIGHT : '11', ACTION_DOWN: '15', ACTION_LEFT: '10'},
    '12': {ACTION_UP : '08', ACTION_RIGHT : '13', ACTION_DOWN: '12', ACTION_LEFT: '12'},
    '13': {ACTION_UP : '09', ACTION_RIGHT : '14', ACTION_DOWN: '13', ACTION_LEFT: '12'},
    '14': {ACTION_UP : '10', ACTION_RIGHT : '15', ACTION_DOWN: '14', ACTION_LEFT: '13'},
    '15': {ACTION_UP : '15', ACTION_RIGHT : '15', ACTION_DOWN: '15', ACTION_LEFT: '15'},
}


# Parameters that are affected by the direct reinforcement learning step

# In[5]:

state_action_value_pairs = {
    '00': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '01': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '02': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '03': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '04': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '05': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '06': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '07': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '08': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '09': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '10': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '11': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '12': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '13': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '14': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
    '15': {ACTION_UP : 1, ACTION_RIGHT : 1, ACTION_DOWN: 1, ACTION_LEFT: 1},
}

# We initialize our policy. We initialize our state action values with all optimistic values so that we don't get stuck at any deadlocks.
greedy_policy = {
    '00': ACTION_UP,
    '01': ACTION_UP,
    '02': ACTION_UP,
    '03': ACTION_UP,
    '04': ACTION_UP,
    '05': ACTION_UP,
    '06': ACTION_UP,
    '07': ACTION_UP,
    '08': ACTION_UP,
    '09': ACTION_UP,
    '10': ACTION_UP,
    '11': ACTION_UP,
    '12': ACTION_UP,
    '13': ACTION_UP,
    '14': ACTION_UP,
    '15': ACTION_UP,
}


# All model related variables in Dyna architecture

# In[6]:

model_state_action_value_pairs = {
    '00': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '01': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '02': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '03': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '04': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '05': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '06': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '07': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '08': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '09': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '10': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '11': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '12': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '13': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '14': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
    '15': {ACTION_UP : (), ACTION_RIGHT : (), ACTION_DOWN: (), ACTION_LEFT: ()},
}


# In[7]:

def updatePolicy():
    for state, action_values in state_action_value_pairs.items():
        highest_valued_action = ACTION_UP
        highest_value = action_values[ACTION_UP]
        if highest_value < action_values[ACTION_RIGHT]:
            highest_valued_action = ACTION_RIGHT
            highest_value = action_values[ACTION_RIGHT]
        if highest_value < action_values[ACTION_DOWN]:
            highest_valued_action = ACTION_DOWN
            highest_value = action_values[ACTION_DOWN]
        if highest_value < action_values[ACTION_LEFT]:
            highest_valued_action = ACTION_LEFT
            highest_value = action_values[ACTION_LEFT]
            
        greedy_policy[state] = highest_valued_action

def chooseActionStochastically():
    random_throw = random.uniform(0, 1)
    if random_throw < 0.25:
        return ACTION_UP
    elif random_throw < 0.5:
        return ACTION_RIGHT
    elif random_throw < 0.75:
        return ACTION_DOWN
    else:
        return ACTION_LEFT
    
def takeAction(state, action):
    reward = immediate_state_rewards[state][action]
    next_state = all_transitions[state][action]
    return next_state, reward

def printPolicy():
    print("Updated Policy", end = '')
    for state in all_states:
        if (int(state) % 4) == 0:
            print("\n")
        print(state, "::", greedy_policy[state],"\t", end = '')
    print("\n\n")


# In[8]:

EPSILON = 1

#Number of episodes to consider
TOTAL_EPISODES_TO_CONSIDER = 200

#Maximum allowed episode length
MAXIMUM_EPISODE_LENGTH = 300

#Number of planning steps
NUMBER_PLANNING_STEPS = 50



all_observed_state_action_pairs = set()

for episode_iterator in range(TOTAL_EPISODES_TO_CONSIDER):
    
    EPSILON = (1/((0.1 * episode_iterator) + 1))
    
    current_state = START_STATE
    current_episode_length = 0
    while(current_state != END_STATE and current_episode_length < MAXIMUM_EPISODE_LENGTH):
        current_episode_length += 1
        
        random_throw = random.uniform(0, 1)
        if random_throw < EPSILON:
            current_action = chooseActionStochastically()
        else:
            current_action = greedy_policy[current_state]
    
        next_state, reward = takeAction(current_state, current_action)
        
        state_action_value_pairs[current_state][current_action] = state_action_value_pairs[current_state][current_action] + (ALPHA * (reward + (GAMMA * state_action_value_pairs[next_state][greedy_policy[next_state]]) - state_action_value_pairs[current_state][current_action]))
        
        all_observed_state_action_pairs.add((current_state, current_action))
        
        model_state_action_value_pairs[current_state][current_action] = (reward, next_state)
        
        for planning_iterator in range(NUMBER_PLANNING_STEPS):
            random_picker = int(random.uniform(0, len(all_observed_state_action_pairs)))
            state_action_pair = list(all_observed_state_action_pairs)[random_picker]
            _state = state_action_pair[0]
            _action = state_action_pair[1]
            _reward, _next_state = model_state_action_value_pairs[_state][_action]
            
            state_action_value_pairs[_state][_action] = state_action_value_pairs[_state][_action] + (ALPHA * (_reward + (GAMMA * state_action_value_pairs[_next_state][greedy_policy[_next_state]]) - state_action_value_pairs[_state][_action]))
        
        if next_state == END_STATE:
            print("Validated")

        current_state = next_state
        updatePolicy()
        
printPolicy()        


# In[ ]:


