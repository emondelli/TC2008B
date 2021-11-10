# Class definition for Model to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import Model
from mesa.datacollection import DataCollector
from agent import RoombaAgent, DirtyAgent
import random
import time

def computeClean(model):
    """Function that, given the model, calculates the percentage of clean tiles in its grid"""
    numDirty = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DirtyAgent):
            numDirty += 1
    # calculate percentage of clean cells
    return 100 - (numDirty/(model.grid.width*model.grid.height)*100)

def writeTxt(fileName, string):
    """Function that, given a file name and a string, writes said string into the file"""
    with open(fileName, "a+") as file:
        file.write(string)


class RandomModel(Model):
    """ Model for Roomba simulation """
    def __init__(self, N, width, height, dirtyPercent, timeLimit):
        self.numAgents = N
        self.grid = MultiGrid(width, height, False) #No torus
        self.schedule = RandomActivation(self)
        self.running = True # For visualization
        self.startTime = None # For keeping track of time
        self.timeLimit = timeLimit # To stop the model from running after a certiain amount of time
        self.dirtyPercent = dirtyPercent
        self.numDirty = int((width*height)*(dirtyPercent/100))
        
        # Add dirty agents to grid
        for i in range(self.numDirty):
            a = DirtyAgent(i, self) # create instance of dirty agent
            self.schedule.add(a) # add it to the schedule

            randomPos = (random.randint(0, width-1), random.randint(0, height-1)) # generate a random position
            count = 1
            while count > 0: # generate a new randomPos while there is a DirtyAgent in randomPos
                count = 0
                agents_in_cell = self.grid.get_cell_list_contents([randomPos])
                for agent in agents_in_cell:
                    if isinstance(agent, DirtyAgent):
                        randomPos = (random.randint(0, width-1), random.randint(0, height-1))
                        count += 1

            self.grid.place_agent(a, randomPos) # place DirtyAgent in randomPos that isn't already dirty

        for i in range(self.numAgents):
            a = RoombaAgent(i+1000, self) #create instance of RoombaAngent with unique id starting from 1000
            self.schedule.add(a) # add it to the schedule
            
            self.grid.place_agent(a, (1, 1)) # place all Roombas at pos (1, 1)
        
        modelReporters = {
            "Time": lambda m: time.time() - m.startTime,
            "Clean Percent": computeClean,
            "Dirty Percent": lambda m: 100 - computeClean(m),
            "Agent Moves": lambda m: [(agent.unique_id, agent.numMoves) for agent in m.schedule.agents if isinstance(agent, RoombaAgent)]
        }

        self.datacollector = DataCollector(modelReporters)

    def step(self):
        '''Advance the model by one step.'''
        if not self.startTime:
            self.startTime = time.time()
        
        self.datacollector.collect(self) # collect data from each step
        self.schedule.step()

        if time.time() - self.startTime > self.timeLimit:
            self.datacollector.collect(self)
            self.running = False # stop running if time limit has been reached
            df = self.datacollector.get_model_vars_dataframe()
            writeTxt("data.txt",
            f"""Number of Roombas: {self.numAgents}, Starting Clean %: {100 - self.dirtyPercent}, Time Limit (seconds): {self.timeLimit}
Execution Time (Time limit reached): {df.iat[-1, 0]}
Clean %: {df.iat[-1, 1]}
Agent Moves: {df.iat[-1, 3]}\n\n""")
        
        count = 0
        for agent in self.schedule.agents: # count how many dirty agents in the grid
            if isinstance(agent, DirtyAgent):
                count += 1
        
        if count == 0: # stop running if there are 0 dirty agents left
            self.datacollector.collect(self)
            self.running = False
            df = self.datacollector.get_model_vars_dataframe()
            writeTxt("data.txt",
            f"""Number of Roombas: {self.numAgents}, Starting Clean %: {100 - self.dirtyPercent}, Time Limit (seconds): {self.timeLimit}
Execution Time (All Clean): {df.iat[-1, 0]}
Clean %: {df.iat[-1, 1]}
Agent Moves: {df.iat[-1, 3]}\n\n""")
