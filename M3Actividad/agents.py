import mesa

class Traffic_Light(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = 0
        self.time = 0
        self.initiate = False
    
    def step(self):
        self.time += 1
        # print("State: ", self.state, " Time: ", self.time)
        if self.time == 10:
            self.state = 1
        if self.time == 20:
            self.state = 0
            self.time = 0

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, model, direction):
        super().__init__(unique_id, model)
        # positions = {'right': (21, 11), 'left': (0, 10), 'up': (10, 21), 'down': (11, 0)}        
        # self.lane = lane
        # # self.vehicleType = vehicleType
        # self.direction_num = direction_num
        self.direction = direction
        # self.x = x[direction][lane]
        # self.y = y[direction][lane]
        self.crossed = 0

    def move(self):
        if self.direction == 'left':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x + 1, y))
        elif self.direction == 'right':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x - 1, y))
        elif self.direction == 'down':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x, y + 1))
        else:
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x, y - 1))


    def step(self):
        self.move()

class Sidewalk(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = 0
        self.time = 0

    def step(self):
        self.time += 1
        if self.time == 10:
            self.state = 1
        if self.time == 20:
            self.state = 0
            self.time = 0