from Map import Map
from Animal import Animal
from Predator import Predator
from Prey import Prey
from SensoryRange import SensoryRange
import random
from IPython.display import clear_output
import matplotlib.pyplot as plt
import numpy as np
from Visualization import Visualization
import time
import pygame
from AnimalParams import SimulationParams, MapParams, AnimalParams

# animal movement showing up on the grid
# animal interaction
# boundaries for map and animal movement
# generate map


class Simulation():

    def __init__(self, simulationParams, mapParams, predatorParams,
                 preyParams):
        self.simulationParams = simulationParams
        self.mapParams = mapParams
        self.predatorParams = predatorParams
        self.preyParams = preyParams
        self.mapSize = (mapParams.sizeX, mapParams.sizeY)
        self.map = Map(self.mapParams, self.predatorParams, self.preyParams)
        self.visualization = Visualization(self.mapSize)

    def simulationLoop(self, t):
        # TESTING
        maxFoodTotal = 0
        animalCount = 0
        diedCount = 0

        # Map.get_next_animal() -> either animal object or None

        animal = self.map.getNextAnimal()
        while animal != None:
            animalSr = SensoryRange()

            #get data surrounding animal
            nearbyPlants = self.map.getNearbyPlants(animal)
            animalSr.setNearbyPlants(nearbyPlants)
            nearbyPredators = self.map.getNearbyPredators(animal)
            nearbyPrey = self.map.getNearbyPrey(animal)
            animalSr.setNearbyPredators(nearbyPredators)
            animalSr.setNearbyPrey(nearbyPrey)
            nearbyTiles = self.map.getNearbyWater(animal)
            nearbyViableMates = self.map.getViableMates(animal)
            animalSr.setNearbyMates(nearbyViableMates)

            animalSr.setNearbyWater(nearbyTiles)
            temp = self.map.getTemp()
            animalSr.setTemp(temp)

            #pass data to animal and receive actions
            animalObj = self.map.convertIDtoAnimal(animal)
            if animalObj.isPrey:
                actions = animalObj.preyReact(animalSr)
            else:
                actions = animalObj.predReact(animalSr)

            #carry out actions

            survives = True
            for action in actions:

                if (action.type == "eat"):
                    if action.foodType == "animal":

                        id = self.map.map[action.foodLocation[1]][
                            action.foodLocation[0]].animalID
                        #print("Animal " + str(id) + " eaten by " + str(animal))
                        #if id == animal:
                        #print("Error: animal eats itself")
                        self.map.deleteAnimal(id)
                    elif action.foodType == "plant":
                        self.map.deletePlant(action.foodLocation)

                elif (action.type == "move"):
                    if (self.map.locToTile(action.endLocation).hasPrey
                            or self.map.locToTile(action.endLocation).hasPred):
                        continue

                    self.map.moveAnimal(animal, action.endLocation)
                    #position x, position y

                elif (action.type == "reproduce"):
                    #print("Animal born at " + str(action.birthLocation))
                    # set parameters of new animal
                    whichParent = random.randint(0, 1)
                    if whichParent == 0:
                        newParams = self.map.locToAnimal(action.selfLocation).animalParams
                    else:
                        newParams = self.map.locToAnimal(action.partnerLocation).animalParams
                    
                    # randomization (PLACEHOLDER)
                    newParams.maxFood = max(newParams.maxFood + random.randint(-25, 25), 0)
                    # print("new animal has max food ", newParams.maxFood)
 
                    if animalObj.isPrey:
                        self.map.createPrey(action.birthLocation, newParams)
                    else:
                        self.map.createPredator(action.birthLocation, newParams)

                    self.map.locToAnimal(
                        action.partnerLocation).resetReprDelay()

                elif (action.type == "drink"):
                    pass  #no action needed
                elif (action.type == "die"):
                    #print("Animal " + str(animal) + " died")
                    self.map.deleteAnimal(animal)
                    survives = False
                    break  #remove from map, delete animal
                else:
                    print("Invalid action type")
                    exit(1)

            if survives:
                self.map.nextOrder.append(animal)

            animalObj.age += 1
            animalObj.reprDelay += 1

            #end of animal loop
            if(animalObj.alive == True):
                maxFoodTotal = maxFoodTotal + animalObj.animalParams.maxFood
                animalCount = animalCount + 1
            else:
                diedCount = diedCount + 1

            animal = self.map.getNextAnimal()

        #Food
        self.map.generatePlants()

        print(animalCount, "animals with average maxFood: ", maxFoodTotal/max(0.1, animalCount))
        print("animals died:", diedCount)

    def visualize(self):
        animalMap = []
        for row in self.map.map:
            rowData = []
            for tile in row:
                if tile.isPrey():
                    rowData.append("prey")
                elif tile.isPred():
                    rowData.append("pred")
                elif tile.hasPlant:
                    rowData.append("plant")
                elif tile.hasWater:
                    rowData.append("water")
                else:
                    rowData.append("grass")

            animalMap.append(rowData)

        ## update visualization here
        self.visualization.updateMap(animalMap)
        self.map.predatorCount.append(self.map.getNumPredators())
        self.map.preyCount.append(self.map.getNumPrey())

        ## Time before switching screens
        pygame.time.wait(self.simulationParams.simulationSpeed)

    def runSimulation(self):

        numPredators = [self.map.getNumPredators()]
        numPrey = [self.map.getNumPrey()]
        timeGraph = [0]

        self.visualize()

        t = 0
        while t < self.simulationParams.simulationLength:
            self.simulationLoop(t)
            t += 1
            # Visualize Current Simulation State
            timeGraph.append(t)
            numPredators.append(self.map.getNumPredators())
            numPrey.append(self.map.getNumPrey())

            self.visualize()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

        self.map.createGraph()
