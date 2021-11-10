# Server setup for visualization of the random Roomba simulation
# Author: Enrique Mondelli A01379363
# Last Modification: 9/11/2021

from model import RandomModel, RoombaAgent
from mesa.visualization.modules import CanvasGrid, PieChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    """Function that defines how each Agent is going to be portrayed visualy"""
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0}

    if isinstance(agent, RoombaAgent):
        portrayal["Color"] = "red"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    
    else:
        portrayal["Color"] = "#944300"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    

    return portrayal


modelParams = {
    "N": UserSettableParameter(param_type="slider", name="Number of Roombas", value=10, min_value=1, max_value=20, step=1),
    "width": 10,
    "height": 10,
    "dirtyPercent": UserSettableParameter("slider", "Percentage of Dirty Cells", 50, 0, 100, 1),
    "timeLimit": UserSettableParameter("slider", "Time limit (seconds)", 30, 0, 120, 1)}

grid = CanvasGrid(agent_portrayal, modelParams["width"], modelParams["height"], 500, 500)

pieChart = PieChartModule([{"Label": "Clean Percent", "Color": "#D5D5D5"}, {"Label": "Dirty Percent", "Color": "#944300"}])
chart = ChartModule([{"Label": "Clean Percent", "Color": "#D5D5D5"}, {"Label": "Dirty Percent", "Color": "#944300"}])

server = ModularServer(RandomModel,
                       [grid, pieChart, chart],
                       "Roomba Room Cleaning Simulation",
                       modelParams)

server.port = 8521 # The default
server.launch()