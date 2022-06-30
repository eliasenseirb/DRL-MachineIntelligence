import random
import json
import ast

class QLearn:
    def __init__(self, actions, epsilon, alpha, gamma):
        self.q = {}
        self.epsilon = epsilon  # exploration constant
        self.alpha = alpha      # discount constant
        self.gamma = gamma      # discount factor
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        '''
        Q-learning:
            Q(s, a) += alpha * (reward(s,a) + max(Q(s') - Q(s,a))            
        '''
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state, return_q=False):
        q = [self.getQ(state, a) for a in self.actions]
        maxQ = max(q)

        if random.random() < self.epsilon:
            minQ = min(q); mag = max(abs(minQ), abs(maxQ))
            # add random values to all the actions, recalculate maxQ
            q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] 
            maxQ = max(q)

        count = q.count(maxQ)
        # In case there're several state-action max values 
        # we select a random one among them
        if count > 1:
            best = [i for i in range(len(self.actions)) if q[i] == maxQ]
            i = random.choice(best)
        else:
            i = q.index(maxQ)

        action = self.actions[i]        
        if return_q: # if they want it, give it!
            return action, q
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

    # only loading q, hyperparameters are not saved 
    def saveModel(self, savedir, iteration):
        print("SAVING MODEL.........................................................................")
        name = "model" + str(iteration) + ".json"
        print(savedir)
        print(name)
        f = open(savedir + "/" + name, "w")
        f.write(str(self.q))
        f.close()
        print("SAVING HYPERPARAMETERS.........................................................................")
        name_hyper = "Hyperparameters" + str(iteration) + ".json"
        f = open(savedir + "/" + name_hyper, "w")
        f.write(str(self.epsilon))
        f.write("\n" + str(self.alpha))
        f.write("\n" +str(self.gamma))
        f.close()

        


    # only loading q, hyperparameters are not saved 
    def loadModel(self, savedir, name):
        print("LOADING MODEL.........................................................................")
        print(savedir + "/" + name)
        f = open(savedir + "/" + name, "r")
        self.q = ast.literal_eval(f.read())
        print(self.q)
        f.close()
        print("LOADING HYPERPARAMETERS.........................................................................")
        name_hyper = "Hyperparameters" + name[5:8] + ".json"
        f = open(savedir + "/" + name_hyper, "r")
        Lines = f.readlines()
        self.epsilon = float(Lines[0])
        self.alpha = float(Lines[1])
        self.gamma = float(Lines[2])
        print(self.q)
        f.close()