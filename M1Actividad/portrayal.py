from agents import *
def portrayal(agent):
    if isinstance(agent, Trash):
        # Trash
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.25, 
                    "Color": "gray", 
                    "Layer": 0}
    else:
        # VacuumCleaner
        portrayal = {"Shape": "aspiradora.png",
                    "Filled": "true",
                    "r": 0.5, 
                    "Color": "blue", 
                    "Layer": 1}

    return portrayal