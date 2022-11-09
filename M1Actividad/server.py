import mesa

from model import *
from portrayal import portrayal

# --------------- Para simular el modelo en servidor ---------------
grid = mesa.visualization.CanvasGrid(portrayal, 10, 10, 500, 500)

# Basura restante
chart = mesa.visualization.ChartModule(
    [{"Label": "Trash_remaining", "Color": "Black"}],
    data_collector_name='datacollector')

# Porcentaje de limpieza
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": "Clean_cells", "Color": "Blue"},
    {"Label": "Dirty_cells", "Color": "Gray"}],
    data_collector_name='datacollector')

server = mesa.visualization.ModularServer(
    CleaningModel, [grid, chart, pie_chart], "Vacuum Cleaner Model", {"NT": 20, "NV": 5, "width": 10, "height": 10, "max_steps": 30}
)
server.port = 8521  # The default
server.launch()