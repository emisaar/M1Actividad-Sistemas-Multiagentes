import mesa

class Trash(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = 0

class VacuumCleaner(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned = 1
        self.collected = 0
        self.move_count = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.move_count += 1

    def step(self):
        self.move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cellmates:
            if (isinstance(obj, Trash)):
                trash = obj
                self.collected += 1
                # print("Agente", self.unique_id, "recogió basura ", self.collected)
                self.model.grid.remove_agent(trash)