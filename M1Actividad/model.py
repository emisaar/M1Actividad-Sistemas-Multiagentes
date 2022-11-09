import mesa
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from agents import *

class CleaningModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, NT, NV, width, height, max_steps):
        self.num_trashes = NT
        self.num_vacuums = NV
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.max_steps_running = max_steps

        # Create VacuumCleaner agents
        for i in range(self.num_trashes):
            a = Trash(i, self)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        for j in range(self.num_vacuums):
            a = VacuumCleaner(j, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = 0
            y = 9
            self.grid.place_agent(a, (x, y))

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Trash_remaining": self.count_trash,
                "Clean_cells": self.get_cleaning_percentage,
                "Dirty_cells": self.get_dirty_percentage,
            },

            agent_reporters={
                # "Vacuum": [agent.unique_id for agent in self.schedule.agents if isinstance(agent, VacuumCleaner)],
                # "Trash_collected": lambda a: a.collected,
            }
        )

    def run_model(self):
        while self.running:
            self.step()

    def step(self):
        self.datacollector.collect(self)
        # Si supera límite de pasos => terminar
        if self.schedule.steps > self.max_steps_running:
            self.running = False
            # print("Límite de pasos alcanzado")
            # print("Número de aspiradoras: ", self.num_vacuums)
            # print("Basura inicial: ", self.num_trashes)
            # print("Basura restante:",self.count_trash())
            # print("Porcentaje de limpieza:", self.get_cleaning_percentage(), "%")
            # print("Total de movimientos:",self.get_total_moves())
            # print("Total de movimientos por agentes:",self.get_moves_per_agent())

        # Si no hay más basura => terminar
        elif self.is_cleaned():
            self.running = False
            # print("Limpieza completa")
            # print("Número de aspiradoras: ", self.num_vacuums)
            # print("Basura inicial: ", self.num_trashes)
            # print("Basura restante:",self.count_trash())
            # print("Porcentaje de limpieza:", self.get_cleaning_percentage(), "%")
            # print("Total de movimientos:",self.get_total_moves())
            # print("Total de movimientos por agentes:",self.get_moves_per_agent())
        else:
            self.schedule.step()

    def is_cleaned(self):
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(obj, Trash) for obj in cell_content):
                return False
        return True

    def count_trash(self):
        count = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(obj, Trash) for obj in cell_content):
                count += 1
        return count

    def get_cleaning_percentage(self): 
        total_cells = self.grid.width * self.grid.height
        return (total_cells - self.count_trash()) / total_cells * 100

    def get_dirty_percentage(self):
        total_cells = self.grid.width * self.grid.height
        return self.count_trash() / total_cells * 100

    def get_total_moves(self):
        total_moves = 0
        for agent in self.schedule.agents:
           total_moves += agent.move_count
        return total_moves

    def get_moves_per_agent(self):
        moves = []
        for agent in self.schedule.agents:
            moves.append(agent.move_count)
        return moves

# Parameters for running the model n times
params = {
    "width": 10, 
    "height": 10, 
    "NT": range(10, 51, 10),
    "NV": range(5, 16, 5), 
    "max_steps": 30
    }

# Using batch_run for running the model 100 times
results = mesa.batch_run(
    CleaningModel,
    parameters=params,
    iterations=100,
    # max_steps=100,
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
    columns=['iteration', 'NT', 'NV', 'Clean_cells'],max_rows=10)
    )

#---- Plotting -----
# Scatterplot de Iteración vs Porcentaje de celdas limpias
# Consideraciones:
    # NT = 50
    # NV = 15
    # Para todas las iteraciones corridas del modelo
sns.set_theme()
sns.scatterplot(
    data = grouped_iterations,
    x="iteration", y="Clean_cells",
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

# Lineplot de Steps vs Clean_cells
df4 = pd.DataFrame()
for i in range(10,110, 25):
    few_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 5) & (results_df.NT == 30)]
    mid_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 10) & (results_df.NT == 30)]
    many_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 15) & (results_df.NT == 30)]
    a = pd.concat([few_vacuums_df, mid_vacuums_df, many_vacuums_df])
    df4 = df4.append(a)

print(df4.to_string(
    index=False, 
    columns=['iteration', 'Step', 'NT', 'NV', 'Clean_cells', 'Dirty_cells'],max_rows=10)
    )

#---- Plotting -----
# Consideraciones:
    # NT = 30 (Para todos los casos)
    # NV = 5, 10, 15
sns.set_theme()
sns.lineplot(
    data = df4,
    x="Step", y="Clean_cells", hue="NV"
)
plt.show()

df5 = pd.DataFrame()
for i in range(10,110, 25):
    few_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 5) & (results_df.NT == 30) & (results_df.Step == 30)].tail(1)
    mid_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 10) & (results_df.NT == 30) & (results_df.Step == 30)].tail(1)
    many_vacuums_df = results_df[(results_df.iteration == i) & (results_df.NV == 15) & (results_df.NT == 30) & (results_df.Step == 30)].tail(1)
    a = pd.concat([few_vacuums_df, mid_vacuums_df, many_vacuums_df])
    df5 = df5.append(a)

print(df5.to_string(
    index=False, 
    columns=['iteration', 'Step', 'NT', 'NV', 'Clean_cells', 'Dirty_cells'],max_rows=10)
    )

# Barplot de Clean_cells vs Iteration (Steps necesarios para limpiar o que se acabe el tiempo)
#---- Plotting -----
# Consideraciones:
    # NT = 30 (Para todos los casos)
    # NV = 5, 10, 15

sns.set_theme()
sns.barplot(
    data = df5,
    x="iteration", y="Clean_cells", hue="NV"
)
plt.show()