import mesa

from model import *
from portrayal import portrayal

# --------------- Para simular el modelo en servidor ---------------
grid = mesa.visualization.CanvasGrid(portrayal, 22, 22, 500, 500)

server = mesa.visualization.ModularServer(
    Intersection_Model, [grid], "Traffic Intersection Model", {"width": 22, "height": 22}
)
server.port = 8521  # The default
server.launch()