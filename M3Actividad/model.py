import mesa
import random
from agents import *

lights_positions = [ (12, 12), (9, 12), (9, 9), (12, 9)] # 1, 2, 3, 4
vehicle_start_positions = {'right': (21, 11), 'left': (0, 10), 'up': (10, 21), 'down': (11, 0)}
flags = [(15, 11), (10, 15), (6, 10), (11, 6)] # 1, 2, 3, 4
class Intersection_Model(mesa.Model):
    
    def __init__(self, width, height):
        self.max_steps = 100
        self.running = True
        self.num_traffic_lights = 4
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)

        self.createStreet()
    
    def run_model(self):
        while self.running:
            self.step()

    def step(self):
        if self.schedule.steps > self.max_steps:
            self.running = False
        else:
            self.schedule.step()
            # Check if there are any vehicles in the intersection
            for i in range(len(flags)):
                if not self.is_Vehicle(flags[i]):
                    self.schedule.agents[i].state = 0 # Yellow
                else:
                    self.schedule.agents[i].state = 1 # Green
                    for j in range(len(flags)):
                        if j != i:
                            print(i, "diff", j)
                            self.schedule.agents[j].state = 2 # Red

    def is_Vehicle(self, pos):
        agents = self.grid.get_cell_list_contents([pos])
        for agent in agents:
            if isinstance(agent, Vehicle):
                return True
        return False

    def createVehicles(self):
        temp = random.randint(0, 99)
        direction = ""
        dist = [25, 50, 75, 100]

        if(temp < dist[0]):
            direction = 'right'
        elif(temp < dist[1]):
            direction = 'left'
        elif(temp < dist[2]):
            direction = 'up'
        else:
            direction = 'down'

        vehicle = Vehicle(self, self, direction)
        self.schedule.add(vehicle)
        self.grid.place_agent(vehicle, vehicle_start_positions[direction])

    def createStreet(self):
        # Create Traffic_Light agents
        for i in range(self.num_traffic_lights):
            traffic_light = Traffic_Light(i, self)
            self.schedule.add(traffic_light)
            self.grid.place_agent(traffic_light, lights_positions[i])

        # Create Sidewalk agents
        for i in range(9):
            sidewalk = Sidewalk(i, self)
            # Top Left Sidewalk
            self.grid.place_agent(sidewalk, (0 + i, 12)) 
            self.grid.place_agent(sidewalk, (9, 13 + i))
            # Top Right Sidewalk
            self.grid.place_agent(sidewalk, (12, 13 + i))
            self.grid.place_agent(sidewalk, (13 + i, 12))
            # Bottom Left Sidewalk
            self.grid.place_agent(sidewalk, (9, 0 + i)) 
            self.grid.place_agent(sidewalk, (0 + i, 9)) 
            # Bottom Right Sidewalk
            self.grid.place_agent(sidewalk, (12, 0 + i))
            self.grid.place_agent(sidewalk, (13 + i, 9))

        self.createVehicles()