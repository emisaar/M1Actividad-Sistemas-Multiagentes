from agents import *

def portrayal(agent):
    if isinstance(agent, Traffic_Light):
        # Traffic_Light
        if agent.state == 0:
            portrayal = {"Shape": "img/lights/yellow_light.png",
                        "Filled": "true",
                        "r": 0.25, 
                        "Color": "blue", 
                        "Layer": 0}
        elif agent.state == 1:
            portrayal = {"Shape": "img/lights/green_light.png",
                        "Filled": "true",
                        "r": 0.25, 
                        "Color": "blue", 
                        "Layer": 0}
        else:
            portrayal = {"Shape": "img/lights/red_light.png",
                        "Filled": "true",
                        "r": 0.25, 
                        "Color": "blue", 
                        "Layer": 0}
                        
    elif isinstance(agent, Vehicle):
        # Car
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.5, 
                    "Color": "gray", 
                    "Layer": 1}
    else:
        # Sidewalk
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.1, 
                    "Color": "black", 
                    "Layer": 0}
    return portrayal