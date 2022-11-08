import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from model import *

params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

# results = mesa.batch_run(
#     CleaningModel,
#     parameters=params,
#     iterations=5,
#     max_steps=100,
#     number_processes=1,
#     data_collection_period=1,
#     display_progress=True,
# )

# results_df = pd.DataFrame(results)
# print(results_df.keys())

def portrayal(agent):
    if isinstance(agent, Trash):
        # Trash
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.25, 
                    "Color": "gray", 
                    "Layer": 0}
    else:
        # VacuumCleaner
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.5, 
                    "Color": "blue", 
                    "Layer": 1}

    return portrayal

grid = mesa.visualization.CanvasGrid(portrayal, 10, 10, 500, 500)

chart = mesa.visualization.ChartModule([{"Label": "Gini",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = mesa.visualization.ModularServer(
    CleaningModel, [grid, chart], "Vacuum Cleaner Model", {"N": 20, "width": 10, "height": 10}
)
server.port = 8521  # The default
server.launch()