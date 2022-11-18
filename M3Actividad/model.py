import mesa
import random
from agents import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

lights_positions = [(12, 12), (9, 12), (9, 9), (12, 9)] # 1, 2, 3, 4
directions = ['right', 'left', 'up', 'down']
vehicle_start_positions = {'right': (21, 11), 'left': (0, 10), 'up': (10, 21), 'down': (11, 0)}
flags = [(15, 11), (10, 15), (6, 10), (11, 6)] # 1, 2, 3, 4

class Intersection_Model(mesa.Model):
    
    def __init__(self, width, height, max_steps, obedient):
        self.max_steps = max_steps
        self.running = True
        self.num_traffic_lights = 4
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.prev_green = 10
        self.collisions = 0
        self.obedient = obedient # True = Obedient (Follow lights), False = Non-Obedient

        self.createStreet()

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Collisions": self.is_Collision,
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
        print(self.is_Collision())
        if self.schedule.steps > self.max_steps:
            self.running = False
            print(self.collisions)
        else:
            if self.schedule.steps < 6:
                self.grid.move_agent(self.schedule.agents[8], (0, 11))
                self.grid.move_agent(self.schedule.agents[9], (21, 10))
                self.grid.move_agent(self.schedule.agents[10], (10, 0))
                self.grid.move_agent(self.schedule.agents[11],(11, 21))

            self.schedule.step()
            # Check if there are any vehicles in the intersection
            for i in range(len(flags)):
                if self.schedule.agents[i].initiate == False:
                    if not self.is_Vehicle(flags[i]):
                        self.schedule.agents[i].state = 0 # Yellow
                    else:
                        self.schedule.agents[i].state = 1 # Green
                        self.schedule.agents[i].initiate = True
                        self.prev_green = self.schedule.agents[i].unique_id 
                        
                        for j in range(len(flags)):
                            if j != i:
                                self.schedule.agents[j].state = 2 # Red
                                self.schedule.agents[j].initiate = True
                        break
                else:
                    pass

            # Change traffic lights
            self.Lights_Logic()

            if self.obedient == True:
                # Move vehicles
                self.Vehicle_Logic()
            else:
                pass

    # Create vehicles
    def createVehicles(self):
        for i in range(4):
            speed = random.randint(1, 2)
            vehicle = Vehicle(i, self, directions[i], speed)
            self.schedule.add(vehicle)
            self.grid.place_agent(vehicle, vehicle_start_positions[directions[i]])
        
        for i in range(4):
            speed = random.randint(2, 3)
            vehicle = Vehicle(i + 10, self, directions[i], speed)
            self.schedule.add(vehicle)
            self.grid.place_agent(vehicle, vehicle_start_positions[directions[i]])


    # Count Collisions
    def is_Collision(self):
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if (x == 11 and y == 11) or (x == 10 and y == 11) or (x == 10 and y == 10) or (x == 11 and y == 10):
                if (len(cell_content) > 1):
                    self.collisions += 1
        return self.collisions


    # Look for vehicles in the intersection
    def is_Vehicle(self, pos):
        agents = self.grid.get_cell_list_contents([pos])
        for agent in agents:
            if isinstance(agent, Vehicle):
                return True
        return False

    
    # Choose next green traffic light
    def Lights_Logic(self):
        print("prev_green",self.prev_green)
        if(self.schedule.agents[0].state == 1 and self.schedule.agents[0].unique_id == self.prev_green):
            self.schedule.agents[0].next_green = False
            self.schedule.agents[1].next_green = True
            self.prev_green = 101
        elif(self.schedule.agents[1].state == 1 and self.schedule.agents[1].unique_id == self.prev_green):
            self.schedule.agents[1].next_green = False
            self.schedule.agents[2].next_green = True
            self.prev_green = 102
        elif(self.schedule.agents[2].state == 1 and self.schedule.agents[2].unique_id == self.prev_green):
            self.schedule.agents[2].next_green = False
            self.schedule.agents[3].next_green = True
            self.prev_green = 103
        elif(self.schedule.agents[3].state == 1 and self.schedule.agents[3].unique_id == self.prev_green):
            self.schedule.agents[3].next_green = False
            self.schedule.agents[0].next_green = True
            self.prev_green = 100
    
    # Move || stop vehicles
    def Vehicle_Logic(self):
            # RIGHT VEHICLE
        x, y = self.schedule.agents[4].pos
        if(self.schedule.agents[0].state == 2 and x <= 13 and x >= 12):
            self.schedule.agents[4].stop_flag = True
        else:
            self.schedule.agents[4].stop_flag = False
        
        x, y = self.schedule.agents[8].pos
        if(self.schedule.agents[0].state == 2 and x <= 13 and x >= 12):
            self.schedule.agents[8].stop_flag = True
        else:
            self.schedule.agents[8].stop_flag = False

        # LEFT VEHICLE
        x, y = self.schedule.agents[5].pos
        if(self.schedule.agents[2].state == 2 and x >= 8 and x <= 9):
            self.schedule.agents[5].stop_flag = True
        else:
            self.schedule.agents[5].stop_flag = False
        
        x, y = self.schedule.agents[9].pos
        if(self.schedule.agents[2].state == 2 and x >= 8 and x <= 9):
            self.schedule.agents[9].stop_flag = True
        else:
            self.schedule.agents[9].stop_flag = False

        # UP VEHICLE
        x, y = self.schedule.agents[6].pos
        if(self.schedule.agents[1].state == 2 and y <= 13 and y >= 12):
            self.schedule.agents[6].stop_flag = True
        else:
            self.schedule.agents[6].stop_flag = False

        x, y = self.schedule.agents[10].pos
        if(self.schedule.agents[1].state == 2 and y <= 13 and y >= 12):
            self.schedule.agents[10].stop_flag = True
        else:
            self.schedule.agents[10].stop_flag = False

        # DOWN VEHICLE
        x, y = self.schedule.agents[7].pos
        if(self.schedule.agents[3].state == 2 and y >= 8 and y <= 9):
            self.schedule.agents[7].stop_flag = True
        else:
            self.schedule.agents[7].stop_flag = False

        x, y = self.schedule.agents[11].pos
        if(self.schedule.agents[3].state == 2 and y >= 8 and y <= 9):
            self.schedule.agents[11].stop_flag = True
        else:
            self.schedule.agents[11].stop_flag = False

    def createStreet(self):
        # Create Traffic_Light agents
        for i in range(self.num_traffic_lights):
            traffic_light = Traffic_Light(i + 100, self)
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
    
        # for i in range(len(self.schedule.agents)):
        #     print(self.schedule.agents[i].unique_id)

# Parameters for running the model n times
params = {
    "width": 22, 
    "height": 22,
    "max_steps": 100,
    "obedient": False,
    }

# Using batch_run for running the model 100 times
results = mesa.batch_run(
    Intersection_Model,
    parameters=params,
    iterations=100,
    # max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=False,
)

results_df = pd.DataFrame(results)
print(results_df.keys())

df = pd.DataFrame()

for i in range(100):
    it = results_df[(results_df.iteration == i) & (results_df.Step==99)].tail(1)

    df = df.append(it)

print(df.to_string(
    index=False, 
    columns=['iteration', 'Step', 'Collisions'],max_rows=10)
    )

sns.set_theme()
sns.scatterplot(
    data=df,
    x="RunId", y="Collisions",
)

plt.show()
