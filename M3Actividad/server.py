import mesa

from model import *
from portrayal import portrayal

# --------------- Para simular el modelo en servidor ---------------
grid = mesa.visualization.CanvasGrid(portrayal, 22, 22, 500, 500)

chart = mesa.visualization.ChartModule(
    [{"Label": "Collisions", "Color": "Black"}],
    data_collector_name='datacollector')


server = mesa.visualization.ModularServer(
    Intersection_Model, [grid, chart], "Traffic Intersection Model", {"width": 22, "height": 22, "max_steps": 100, "obedient": True}
)
server.port = 8521  # The default
server.launch()