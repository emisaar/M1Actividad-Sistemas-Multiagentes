import mesa

class Traffic_Light(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = 0
        self.time = 0
        self.initiate = False
    
    def step(self):
        if(self.initiate == True):
            self.time += 1
            if(self.state == 1 and self.time == 2): 
                self.state = 0 # Yellow
            if(self.state == 0 and self.time == 4):
                self.state = 2 # Red
                self.time = 0
            if(self.state == 2 and self.time == 2):
                self.state = 2 # Red
            if(self.state == 2 and self.time == 4):
                self.state = 1 # Green
                self.time = 0
                
        
        print("State", self.state)
        print("Time", self.time)
        

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, model, direction, speed):
        super().__init__(unique_id, model)
        self.direction = direction
        self.crossed = 0
        self.speed = speed
        self.stop_flag = False

    def move(self):
        if self.direction == 'left':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x + self.speed, y))
        elif self.direction == 'right':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x - self.speed, y))
        elif self.direction == 'down':
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x, y + self.speed))
        else:
            x, y = self.pos
            # print(x, y)
            self.model.grid.move_agent(self, (x, y - self.speed))

    def stop(self):
        self.pos = self.pos

    def step(self):
        if self.stop_flag == False:
            self.move()
        else:
            print("Stop moving")
            self.stop()

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