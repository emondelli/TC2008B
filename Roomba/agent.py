# Class definition for RoombaAgent and DirtyAgent to be used in the simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from mesa import Agent


class DirtyAgent(Agent):
    """ Agent that represents a dirty cell"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # The agent's step will go here.
        pass 

class RoombaAgent(Agent):
    """ Agent that moves randomly and removes DirtyAgents when in the same cell """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.numMoves = 0

    def move(self):
        """Move funtion to calculate a random position and move Agent to said position"""
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # include diagonal neighbors
            include_center=False) #Doesn't include its own position

        move = True
        newPosition = self.random.choice(possibleSteps) # choose random position to move to
        for agent in self.model.grid.get_cell_list_contents([newPosition]): 
            if isinstance(agent, RoombaAgent): # check whether random postion contains another roomba
                move = False # if it does, it doesn't move
        
        if move:
            self.model.grid.move_agent(self, newPosition) # move roomba to random possible position


    def step(self):
        """ Move randomly in each step and remove DirtyAgents in the cell """
        agentsInCell = self.model.grid.get_cell_list_contents([self.pos])
        move = True
        for agent in agentsInCell: # check contents of cell
            if isinstance(agent, DirtyAgent): # remove DirtyAgents from cell
                self.model.grid._remove_agent(self.pos, agent)
                self.model.schedule.remove(agent)
                move = False
        
        if move: # if roomba removed a DirtyAgent in this step, it doesn't move
            self.move()
            self.numMoves += 1

 
