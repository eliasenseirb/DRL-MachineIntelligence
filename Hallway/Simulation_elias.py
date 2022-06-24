import pygame as pg 
import random
from collections import defaultdict
import time
import numpy as np


#Hallway problem
# ***********
# --*-*-*-G--

#15 rooms with 4 orientations: 60 states
#21 observations 

GREY = (180,180,180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (234, 221, 0)

WITDH = 1100
HEIGHT = 200
#modifies speed of the game
FPS = 60

SIZEX = 11
SIZEY = 2

SQUARE = HEIGHT / 2

TOTAL = 1000




# define a main function
def main():
    pg.init()
    Hallway = [[5,5,5,5,5,5,5,5,5,5,5],
               [0,0,1,0,2,0,3,0,4,0,0]]
    pg.display.set_caption("Hallway Problem")
    screen = pg.display.set_mode((WITDH, HEIGHT))


    #necessary for reseting the agent
    global reward_received
    reward_received = False
    #initilaize Agent
    agent = Agent()
    #initilaize Reward
    reward = Reward()
    #initilaize State
    state = State()
    observation = Observation()
  #  running = True
    clock = pg.time.Clock()

    #Main code start:

    #define training parameters
    epsilon = 0.5 #the percentage of time when we should take the best action (instead of a random action)
    discount_factor = 0.9 #discount factor for future rewards
    learning_rate = 0.9 #the rate at which the AI agent should learn

    #run through 1000 training episodes
    for episode in range(TOTAL):
        if episode == 100:
            epsilon = 0.7
        if episode == 300:
           epsilon = 0.8
        if episode == 500:
            epsilon = 0.9
        if episode == 900:
            epsilon = 0.99
        #get the starting location for this episode
        row_index, column_index = agent.position[1], agent.position[0]

        #continue taking actions (i.e., moving) until we reach a terminal state
        #(i.e., until we reach the item packaging area or crash into an item storage location)
        while not reward.is_terminal_state(row_index, column_index):
          agent.position[0] = column_index
          agent.position[1] = row_index
            
          #draw hallway
          Draw.draw_hallway(screen, Hallway)
         
          #draw agent
          Draw.draw_agent(screen, agent)
          #print("I am in state: " + str(state.return_state(agent)))
          #print("I observe from the environment: " + str(observation.return_observation(state.return_state(agent))))
          for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                
         # print("x = " + str(column_index))
          #print("y = " + str(row_index))
          
            #choose which action to take (i.e., where to move next)
          action_index = agent.get_next_action(row_index, column_index, epsilon)

          #perform the chosen action, and transition to the next state (i.e., move to the next location)
          old_row_index, old_column_index = row_index, column_index #store the old row and column indexes
          row_index, column_index = agent.get_next_location(row_index, column_index, action_index, reward)
          
          
          #receive the reward for moving to the new state, and calculate the temporal difference
          rewardvar = reward.rewards[row_index, column_index]
          old_q_value = agent.q_values[old_row_index, old_column_index, action_index]
          temporal_difference = rewardvar + (discount_factor * np.max(agent.q_values[row_index, column_index])) - old_q_value

          #update the Q-value for the previous state and action pair
          new_q_value = old_q_value + (learning_rate * temporal_difference)
          agent.q_values[old_row_index, old_column_index, action_index] = new_q_value

          if reward_received:
              Draw.draw_hallway(screen, Hallway)
              Draw.draw_agent(screen, agent)
              time.sleep(0.001)
              agent = Agent()
              print("reward : " + str(episode) + "/" + str(TOTAL))
             # print("Resetting the agent")
              reward_received = False
              
          #time.sleep(0.05)
          clock.tick(FPS)
    print('Training complete!')        


    # while running:
    #     #draw hallway
    #     Draw.draw_hallway(screen, Hallway)
    #     # event handling, gets all event from the event queue
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             running = False
    #     #draw agent
    #     Draw.draw_agent(screen, agent)
    #     print("I am in state: " + str(state.return_state(agent)))
    #     print("I observe from the environment: " + str(observation.return_observation(state.return_state(agent))))
    #     #perfom action
    #     Agent.random_action(agent)
    #     #get reward
    #     reward.get_reward(agent)
    #     #resetting the agent
    #     if reward_received:
    #         Draw.draw_hallway(screen, Hallway)
    #         Draw.draw_agent(screen, agent)
    #         time.sleep(1)
    #         agent = Agent()
    #         print("Resetting the agent")
    #         reward_received = False


    #     clock.tick(FPS)

    # #Main code end



#class for drawing the environment and agent
class Draw():
    def draw_hallway(screen, Hallway):
        screen.fill(BLACK)
        #draw Environment
        for i in range(len(Hallway)):
            for j in range(len(Hallway[i])):
                #draw Hallway
                if i == 0:
                    #odd
                    if (i + j) % 2:
                        color = WHITE
                    else:
                        color = GREY
                    pg.draw.rect(screen, color, pg.Rect(j * SQUARE, i * SQUARE, SQUARE, SQUARE))
                
                #draw landmarks and goal
                elif i == 1 and Hallway[i][j] != 0:
                    if Hallway[i][j] == 1:
                        color = RED
                    elif Hallway[i][j] == 2:
                        color = RED
                    elif Hallway[i][j] == 3:
                        color = RED
                    elif Hallway[i][j] == 4:
                        color = YELLOW
                    pg.draw.rect(screen, color, pg.Rect(j * SQUARE, i * SQUARE, SQUARE, SQUARE))




    def draw_agent(screen, agent):
        agent_raw = pg.image.load("agent.png")
        #rotation
        agent_img = pg.transform.rotate(agent_raw, agent.position[2])
        #scaling
        agent_img = pg.transform.scale(agent_img, (SQUARE, SQUARE))
        screen.blit(agent_img, (SQUARE*agent.position[0], SQUARE*agent.position[1]))
        #updates display
        pg.display.flip()	



#five actions possible
#needs position and heading of the agent
# #actions 0:standing still; 1: moving forward; 2: turning right; 3: turning around; 4: turning left 
class Action:
    def  __init__(self):
        self.action_space = [self.stay, self.move, self.turn_right, self.turn_around, self.turn_left]

    def stay(agent):
        print("I am standing still")
        pass
    
    #If the agent hits a landmark or wall he will stay still
    #North: 0; East: 270; South: 180; West: 90
    def move(agent):
        #north
        if agent.position[2] == 0:
            print("I want to move north")
            if agent.position == [2,1,0] or agent.position == [4,1,0] or agent.position == [6,1,0] or agent.position == [8,1,0]:
                agent.position[1] = agent.position[1] - 1
            else:
                print("I hit a wall")
        #west
        elif agent.position[2] == 90:
            print("I want to move west")
            if agent.position[0] != 0 and  agent.position[1] != 1:
                agent.position[0] = agent.position[0] - 1
            else: 
                print("I hit a wall")
        #south
        elif agent.position[2] == 180:
            print("I want to move south")
            if agent.position == [2,0,180] or agent.position == [4,0,180] or agent.position == [6,0,180] or agent.position == [8,0,180]:
                agent.position[1] = agent.position[1] + 1
            else:
                print("I hit a landmark or wall")
        #east
        else:
            print("I want to move east")
            if agent.position[0] != 10 and agent.position[1] != 1:
                agent.position[0] = agent.position[0] + 1
            else: print("I hit a wall")

    def turn_right(agent):
        print("I am turning right")
        if agent.position[2] == 0:
            agent.position[2] = 270
        else:
            agent.position[2] = agent.position[2] - 90

    def turn_left(agent):
        print("I am turning left")
        if agent.position[2] == 270:
            agent.position[2] = 0
        else:
            agent.position[2] = agent.position[2] + 90

    def turn_around(agent):
        print("I am turning around")
        if agent.position[2] == 0 or agent.position[2] == 90:
            agent.position[2] = agent.position[2] + 180
        else:
            agent.position[2] = agent.position[2] - 180
            
        #Define a function that will get the shortest path between any location within the warehouse that 
        #the robot is allowed to travel and the item packaging location.
    def get_shortest_path(start_row_index, start_column_index):
            #return immediately if this is an invalid starting location
        if Reward.is_terminal_state(start_row_index, start_column_index):
            return []
        else: #if this is a 'legal' starting location
            current_row_index, current_column_index = start_row_index, start_column_index
            shortest_path = []
            shortest_path.append([current_row_index, current_column_index])
            #continue moving along the path until we reach the goal (i.e., the item packaging location)
            while not Reward.is_terminal_state(current_row_index, current_column_index):
                #get the best action to take
                action_index = Agent.get_next_action(current_row_index, current_column_index, 1.)
                #move to the next location on the path, and add the new location to the list
                current_row_index, current_column_index = Agent.get_next_location(current_row_index, current_column_index, action_index)
                shortest_path.append([current_row_index, current_column_index])
            return shortest_path



class Agent:
    def __init__(self):
        #North: 0; East: 270; South: 180; West: 90
        #x, y, degree
        #init state object
        state = State()
        #random starting position/state
        self.state = random.randint(1, 56)
        self.position = state.return_position(self.state)
        self.q_values = np.zeros((SIZEY, SIZEX, 4))
        self.actions = ['up', 'right', 'down', 'left']



    #performs random actions
    def random_action(agent):
        action_space = ["stay", "move", "turn_right","turn_left","turn_around"]
        action = random.choice(action_space)
        if action == "stay":
            Action.stay(agent)
        elif action == "move":
            Action.move(agent)
        elif action == "turn_right":
            Action.turn_right(agent)
        elif action == "turn_left":
            Action.turn_left(agent)
        else:
            Action.turn_around(agent)
            
    #define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
    def get_next_action(self, current_row_index, current_column_index, epsilon):
         #if a randomly chosen value between 0 and 1 is less than epsilon, 
         #then choose the most promising value from the Q-table for this state.
        if np.random.random() < epsilon:
            return np.argmax(self.q_values[current_row_index, current_column_index])
        else: #choose a random action
            return np.random.randint(4)
        
    
    
    #define a function that will get the next location based on the chosen action
    def get_next_location(self, current_row_index, current_column_index, action_index, reward):
        new_row_index = current_row_index
        new_column_index = current_column_index
        #print("_____________________")
        if self.actions[action_index] == 'up' and current_row_index > 0:
            if reward.rewards[current_row_index-1,current_column_index] != -100: 
                new_row_index -= 1
                #print("north")
        elif self.actions[action_index] == 'right' and current_column_index < SIZEX - 1:
            if reward.rewards[current_row_index,current_column_index+1] != -100: 
                self.position[2] = 270
                new_column_index += 1
                #print("east")
        elif self.actions[action_index] == 'down' and current_row_index < SIZEY - 1:
            if reward.rewards[current_row_index+1,current_column_index] != -100: 
                self.position[2] = 180
                new_row_index += 1
             #   print("south")
            #else:
              #  print("hit a wall")
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            if reward.rewards[current_row_index,current_column_index-1] != -100: 
                self.position[2] = 90
                new_column_index -= 1
            #print("west")
        return new_row_index, new_column_index

#if the agent is in the goal state/position
#he will recieve +1 reward else -1
class Reward():
    def __init__(self):
        #self.reward = 0
        
        #Create a 2D numpy array to hold the rewards for each state. 
        #The array contains 11 rows and 11 columns (to match the shape of the environment), and each value is initialized to -100.
        self.rewards = np.full((SIZEY, SIZEX), -1.)
        self.rewards[1, 8] = 1000. #set the reward for the packaging area (i.e., the goal) to 100
        for i in range(2):
            self.rewards[1,i] = -100
            self.rewards[1,SIZEX-i-1] = -100
        self.rewards[1,3] = -100
        self.rewards[1,5] = -100
        self.rewards[1,7] = -100
        
        #rewards of the checkpoint
        #self.rewards[1,2] = 0
        #self.rewards[1,4] = 1
        #self.rewards[1,6] = 2
        print(self.rewards)
        
    #define a function that determines if the specified location is a terminal state
    def is_terminal_state(self, current_row_index, current_column_index):
        global reward_received
        #if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
        if self.rewards[current_row_index, current_column_index] == 1000.:
            reward_received = True
            return True    
        else: return False

    
        
        
    # def get_reward(self, agent):
    #     #agent is at the goal state
    #     if agent.position[0] == 8 and agent.position[1] ==1:
    #         self.reward = self.reward + 1
    #         global reward_received
    #         reward_received = True
    #         print("GOAL!!!!")

    #     #do nothing
    #     else:
    #         self.reward = self.reward
    #     print("Current Reward: " + str(self.reward))


class State():
    def __init__(self):
        #list of all states
        #counting from left to right, top to down, north-->east-->south-->west
        #North: 0; East: 270; South: 180; West: 90
        #goal states are 57, 58, 59, 60
        self.state_space = list(range(1,61))

        self.statesToPositions={1: [0,0,0],  2: [0,0,270],  3: [0,0,180],  4: [0,0,90],
                                5: [1,0,0],  6: [1,0,270],  7: [1,0,180],  8: [1,0,90],
                                9: [2,0,0],  10:[2,0,270],  11:[2,0,180],  12:[2,0,90],
                                13:[3,0,0],  14:[3,0,270],  15:[3,0,180],  16:[3,0,90],
                                17:[4,0,0],  18:[4,0,270],  19:[4,0,180],  20:[4,0,90],
                                21:[5,0,0],  22:[5,0,270],  23:[5,0,180],  24:[5,0,90],
                                25:[6,0,0],  26:[6,0,270],  27:[6,0,180],  28:[6,0,90],
                                29:[7,0,0],  30:[7,0,270],  31:[7,0,180],  32:[7,0,90],
                                33:[8,0,0],  34:[8,0,270],  35:[8,0,180],  36:[8,0,90],
                                37:[9,0,0],  38:[9,0,270],  39:[9,0,180],  40:[9,0,90],
                                41:[10,0,0], 42:[10,0,270], 43:[10,0,180], 44:[10,0,90],
                                45:[2,1,0],  46:[2,1,270],  47:[2,1,180],  48:[2,1,90],
                                49:[4,1,0],  50:[4,1,270],  51:[4,1,180],  52:[4,1,90],
                                53:[6,1,0],  54:[6,1,270],  55:[6,1,180],  56:[6,1,90],
                                57:[8,1,0],  58:[8,1,270],  59:[8,1,180],  60:[8,1,90]}

        self.positionsToStates={tuple([0,0,0]):1,   tuple([0,0,270]):2,   tuple([0,0,180]):3,   tuple([0,0,90]):4,
                                tuple([1,0,0]):5,   tuple([1,0,270]):6,   tuple([1,0,180]):7,   tuple([1,0,90]):8,
                                tuple([2,0,0]):9,   tuple([2,0,270]):10,  tuple([2,0,180]):11,  tuple([2,0,90]):12,
                                tuple([3,0,0]):13,  tuple([3,0,270]):14,  tuple([3,0,180]):15,  tuple([3,0,90]):16,
                                tuple([4,0,0]):17,  tuple([4,0,270]):18,  tuple([4,0,180]):19,  tuple([4,0,90]):20,
                                tuple([5,0,0]):21,  tuple([5,0,270]):22,  tuple([5,0,180]):23,  tuple([5,0,90]):24,
                                tuple([6,0,0]):25,  tuple([6,0,270]):26,  tuple([6,0,180]):27,  tuple([6,0,90]):28,
                                tuple([7,0,0]):29,  tuple([7,0,270]):30,  tuple([7,0,180]):31,  tuple([7,0,90]):32,
                                tuple([8,0,0]):33,  tuple([8,0,270]):34,  tuple([8,0,180]):35,  tuple([8,0,90]):36,
                                tuple([9,0,0]):37,  tuple([9,0,270]):38,  tuple([9,0,180]):39,  tuple([9,0,90]):40,
                                tuple([10,0,0]):41, tuple([10,0,270]):42, tuple([10,0,180]):43, tuple([10,0,90]):44,
                                tuple([2,1,0]):45,  tuple([2,1,270]):46,  tuple([2,1,180]):47,  tuple([2,1,90]):48,
                                tuple([4,1,0]):49,  tuple([4,1,270]):50,  tuple([4,1,180]):51,  tuple([4,1,90]):52,
                                tuple([6,1,0]):53,  tuple([6,1,270]):54,  tuple([6,1,180]):55,  tuple([6,1,90]):56,
                                tuple( [8,1,0]):57, tuple([8,1,270]):58,  tuple([8,1,180]):59,  tuple([8,1,90]):60}


    #returns the state from given agent position
    def return_state(self, agent):
        return self.positionsToStates[tuple(agent.position)]

    #returns the position from given state
    def return_position(self, state):
        return self.statesToPositions[state]

#21 observation
#each possible combination of the presence of a wall in aeach of the four relative directions
#plus goal and three landmarks visible while facing south
#North: 0; East: 270; South: 180; West: 90
class Observation():
    def __init__(self):
        #convention 1:Heading 2: front of the agent 3: Right 4: Behind 5: left 
        #x: wall o:empty r: red/landmark g: goal

        #agent position needs to be added to the dictionary 

        self.observationsToStates =   {"nxoxx" : (1),                 "eoxxx" : (2),                  "sxxxo" : (3),                  "wxxox" : (4),
                                       "nxoxo" : (5, 13, 21, 29, 37), "eoxox" : (6, 14, 22, 30, 38),  "sxoxo" : (7, 15, 23, 31, 39),  "woxox" : (8, 16, 24, 32, 40),
                                       "nxooo" : (9, 17, 25, 33),     "eooox" : (10, 18, 26, 34),     "sroxo" : (11, 19, 27),         "woxoo" : (12, 20, 28, 36),
                                                                                                      "sgoxo" : (35),
                                       "nxxxo" : (41),                "exxox" : (42),                 "sxoxx" : (43),                 "woxxx" : (44),
                                       "noxxx" : (45, 49, 53, 57),    "exxxo" : (46, 50, 54, 58),     "sxxox" : (47, 51, 55, 59),     "wxoxx" : (48, 52, 56, 60)}

        self.statesToObservations = {
             1 : "nxoxx",
             2 : "eoxxx",
             3 : "sxxxo",
             4 : "wxxox",
             5 : "nxoxo",
             6 : "eoxox",
             7 : "sxoxo",
             8 : "woxox",
             9 : "nxooo",
            10 : "eooox",
            11 : "sroxo",
            12 : "woxoo",
            13 : "nxoxo",
            14 : "eoxox",
            15 : "sxoxo",
            16 : "woxox",
            17 : "nxooo",
            18 : "eooox",
            19 : "sroxo",
            20 : "woxoo",
            21 : "nxoxo",
            22 : "eoxox",
            23 : "sxoxo",
            24 : "woxox",
            25 : "nxooo",
            26 : "eooox",
            27 : "sroxo",
            28 : "woxoo",
            29 : "nxoxo",
            30 : "eoxox",
            31 : "sxoxo",
            32 : "woxox",
            33 : "nxooo",
            34 : "eooox",
            35 : "sgoxo",
            36 : "woxoo",
            37 : "nxoxo",
            38 : "eoxox",
            39 : "sxoxo",
            40 : "woxox",
            41 : "nxxxo",
            42 : "exxox",
            43 : "sxoxx",
            44 : "woxxx",
            45 : "noxxx",
            46 : "exxxo",
            47 : "sxxox",
            48 : "wxoxx",
            49 : "noxxx",
            50 : "exxxo",
            51 : "sxxox",
            52 : "wxoxx",
            53 : "noxxx",
            54 : "exxxo",
            55 : "sxxox",
            56 : "wxoxx",
            57 : "noxxx",
            58 : "exxxo",
            59 : "sxxox",
            60 : "wxoxx"
        }
    
    #returns the observation based on the agent state
    def return_observation(self, state):
        return self.statesToObservations[state]
    
    
    
    def observe():
        pass



if __name__=="__main__":
    #state = State()
    #print(state.state_space)
    main()