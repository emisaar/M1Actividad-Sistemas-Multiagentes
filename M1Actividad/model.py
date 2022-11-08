import mesa
from agents import *

class CleaningModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_trashes = N
        self.num_vacuums = self.random.randrange(1, N/2)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.max_steps_running = 30

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
                "Trash remaining": self.count_trash,
                "Clean cells": self.get_cleaning_percentage,
                "Dirty cells": self.get_dirty_percentage,
                "Moves per agent": self.get_moves_per_agent,
            },
        )

    def run_model(self):
        while self.running:
            self.step()

    def step(self):
        self.datacollector.collect(self)
        # Si supera límite de pasos => terminar
        if self.schedule.steps + 1 > self.max_steps_running:
            self.running = False
            print("Límite de pasos alcanzado")
            print("Basura inicial: ", self.num_trashes)
            print("Basura restante:",self.count_trash())
            print("Porcentaje de limpieza:", self.get_cleaning_percentage(), "%")
            print("Total de movimientos:",self.get_total_moves())
            print("Total de movimientos por agentes:",self.get_moves_per_agent())

        # Si no hay más basura => terminar
        elif self.is_cleaned():
            self.running = False
            print("Limpieza completa")
            print("Basura inicial: ", self.num_trashes)
            print("Basura restante:",self.count_trash())
            print("Porcentaje de limpieza:", self.get_cleaning_percentage(), "%")
            print("Total de movimientos:",self.get_total_moves())
            print("Total de movimientos por agentes:",self.get_moves_per_agent())
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