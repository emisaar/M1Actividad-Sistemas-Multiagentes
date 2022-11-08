import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from model import *
from portrayal import portrayal

# params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

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

grid = mesa.visualization.CanvasGrid(portrayal, 10, 10, 500, 500)

chart = mesa.visualization.ChartModule(
    [{"Label": "Trash remaining", "Color": "Black"}],
    data_collector_name='datacollector')

chart_moves = mesa.visualization.BarChartModule(
    [{"Label": "Moves per agent", "Color": "Black"}],
    data_collector_name='datacollector')

pie_chart = mesa.visualization.PieChartModule(
    [{"Label": "Clean cells", "Color": "Blue"},
    {"Label": "Dirty cells", "Color": "Gray"}],
    data_collector_name='datacollector')

server = mesa.visualization.ModularServer(
    CleaningModel, [grid, chart, chart_moves, pie_chart], "Vacuum Cleaner Model", {"N": 20, "width": 10, "height": 10}
)
server.port = 8521  # The default
server.launch()

plt.show()