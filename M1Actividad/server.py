import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import agentpy as ap

from model import *
from portrayal import portrayal

# Parameters for running the model n times
params = {"width": 10, "height": 10, "NT": range(10, 51, 10), "NV": range(5, 16, 5)}

# Using batch_run for running the model 100 times
results = mesa.batch_run(
    CleaningModel,
    parameters=params,
    iterations=100,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=False,
)

# Convert results to pandas dataframe
results_df = pd.DataFrame(results)
print(results_df.keys())

# Data is filtered to get only the data at the end of each simulation
grouped_iterations = pd.DataFrame(columns=['iteration','NT', 'NV', 'Trash_remaining', 'Clean_cells', 'Dirty_cells'])
for it, group in results_df.groupby(["iteration"]):
    grouped_iterations = grouped_iterations.append(
        {'iteration':group.iloc[-1].iteration, 
        'NT':group.iloc[-1].NT, 
        'NV':group.iloc[-1].NV, 
        'Trash_remaining':group.iloc[-1].Trash_remaining,
        'Clean_cells':group.iloc[-1].Clean_cells,
        'Dirty_cells':group.iloc[-1].Dirty_cells}, 
        ignore_index=True)
# print(grouped_iterations.to_string(index=False, max_rows=25))
print(grouped_iterations.to_string(
    index=False, 
    columns=['iteration', 'Step', 'NT', 'NV', 'Trash_remaining'],max_rows=10)
    )
# Scatterplot de basura restante vs iteración
# Consideraciones:
    # NT =
    # NV =
    # Para todas las iteraciones corridas del modelo

#---- Plotting -----
sns.set_theme()
sns.scatterplot(
    data = grouped_iterations,
    x="iteration", y="Trash_remaining",
)
plt.show()

# Scatterplot de basura restante vs número de aspiradoras

df2 = pd.DataFrame()

for i in range(10,100, 10):
    few_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 5)].tail(1)
    mid_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 10)].tail(1)
    many_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 15)].tail(1)
    a = pd.concat([few_vacuums_df, mid_vacuums_df, many_vacuums_df])
    df2 = df2.append(a)

print(df2.to_string(
    index=False, 
    columns=['iteration', 'Step', 'NT', 'NV', 'Clean_cells', 'Dirty_cells'],max_rows=10)
    )

#---- Plotting -----
# Consideraciones NV vs Clean_cells:
    # NT = 50 (Para todos los casos)
    # NV = 5, 10, 15

sns.set_theme()
sns.barplot(
    data = df2,
    x="NV", y="Clean_cells", hue="iteration"
)
plt.show()

df3 = pd.DataFrame()

for i in range(10,100, 10):
    few_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NT == 10)].tail(1)
    mid_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NT == 30)].tail(1)
    many_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NT == 50)].tail(1)
    a = pd.concat([few_vacuums_df, mid_vacuums_df, many_vacuums_df])
    df3 = df3.append(a)

print(df3.to_string(
    index=False, 
    columns=['iteration', 'Step', 'NT', 'NV', 'Clean_cells', 'Dirty_cells'],max_rows=10)
    )

#---- Plotting -----
# Consideraciones NT vs Clean_cells:
    # NT = 10, 30, 50
    # NV = 15 (Para todos los casos)
sns.set_theme()
sns.barplot(
    data = df3,
    x="NT", y="Clean_cells", hue="iteration"
)
plt.show()



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
    CleaningModel, [grid, chart, pie_chart], "Vacuum Cleaner Model", {"NT": 20, "NV": 5, "width": 10, "height": 10}
)
server.port = 8521  # The default
# server.launch()