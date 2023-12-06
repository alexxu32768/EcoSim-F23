from Tile import Tile
from Animal import Animal
from Predator import Predator
from Prey import Prey
from Visualization import Visualization
import random
import math
import numpy as np
import copy
import matplotlib.pyplot as plt
from AnimalParams import SimulationParams, MapParams, AnimalParams

# different dictionaries for each variable and then
# we pass in a coordinate to determine what is there
# coordinates will list the characteristics of what
# is there


class Map:
    #called in Simulation
    def __init__(self, mapParams, predatorParams, preyParams):
        self.mapParams = mapParams
        self.predatorParams = predatorParams
        self.preyParams = preyParams

        self.sizeX = mapParams.sizeX
        self.sizeY = mapParams.sizeY
        self.mapSize = (mapParams.sizeX, mapParams.sizeY)  #tuple

        self.currTemp = mapParams.temp
        self.numAnimals = 0
        self.numPredators = 0
        self.numPrey = 0
        self.animalID = 0
        self.map = [[Tile() for i in range(self.sizeX)]
                    for j in range(self.sizeY)]
        
        for i in range(2 + (self.sizeX * self.sizeY) // 250):
            self.pondMaker()
        
        for i in range(1 + (self.sizeX + self.sizeY) // 25):
            self.riverMaker()

        #self.create_graph()

        self.IDtoAnimal = {}
        self.IDtoLoc = {}  # dictionary from animal IDs to locations
        self.currentOrder = [
        ]  # list of animal ID's: specifies order of action
        self.currentIndex = 0
        self.nextOrder = []
        self.predatorCount = []
        self.preyCount = []
        self.predatorCount.append(self.getNumPredators())
        self.preyCount.append(self.getNumPrey())

        self.initializeAnimals()
        self.generateInitialPlants()


    def convertIDtoLoc(self, animalID):
        return self.IDtoLoc[animalID]

    def convertIDtoTile(self, animalID):
        animalLoc = self.convertIDtoLoc(animalID)
        return self.map[animalLoc[1]][animalLoc[0]]

    def convertIDtoAnimal(self, animalID):
        return self.IDtoAnimal[animalID]

    def locToTile(self, loc):
        return self.map[loc[1]][loc[0]]

    def locToAnimal(self, loc):
        return self.IDtoAnimal[self.locToTile(loc).animalID]

    # function that makes a sine function that we
    # can pass back to tile to make curvy rivers
    def riverMaker(self):
        coef = [random.random() for i in range(4)]
        if (coef[3] > 0.75):
            coef[3] = coef[3] - 0.5
        if (coef[3] < 0.25):
            coef[3] = coef[3] + 0.5
        if (coef[0] < 0.5):
            coef[0] = coef[0] + 0.5
        if (coef[1] < 0.5):
            coef[1] = coef[1] + 0.5
        for i in range(self.sizeY):
            j = int(3 * coef[0] * (math.sin(coef[1] * i + coef[2])) +
                    coef[3] * self.sizeX)
            if (j >= 0 and j < self.sizeX):
                self.map[i][j].setWater()

        #return

    def pondMaker(self):
        # generate random spot for pond
        xCord = int(random.randint(0, self.sizeX - 8))
        yCord = int(random.randint(0, self.sizeY - 8))

        # size - height (5-8), width (5-8)
        height = int(random.randint(5, 8))
        width = int(random.randint(5, 8))

        for i in range(width):
            # generating extra dimensions so pond isn't square
            shift = int(random.randint(-2, 2))
            for j in range(height):
                if (yCord + i < self.sizeY and xCord + j + shift < self.sizeX):
                    self.map[yCord + i][xCord + j + shift].setWater()

    def generateInitialPlants(self):
        self.generatePlants(.85)
        return

    def generatePlants(self, threshold=.95):
        # if t = 0, use 0.85 for p threshold. otherwise use 0.95
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if (self.currTemp >= 40 and self.currTemp <= 80) and (
                        self.map[j][i].getTerrain() == "E"):
                    #gets random number between 0 and 1
                    p = random.random()

                    if p > threshold:
                        self.map[j][i].setPlant()

        return

    def deletePlant(self, loc):
        tile = self.locToTile(loc)
        #print("Plant deleted at ", loc)
        tile.hasPlant = False
        tile.terrain = "E"
        return

    def initializeAnimals(self):
        remainPred = self.mapParams.numStartingPredators
        remainPrey = self.mapParams.numStartingPrey
        remainTile = self.sizeX * self.sizeY
        quit = False
        # numpy random may have a more efficient implementation, but this works
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if self.map[j][i].hasWater:
                    remainTile -= 1
                    continue
                p1 = remainPred / (remainTile)
                p2 = (remainPred + remainPrey) / remainTile
                p = np.random.rand()
                newPredator = (p < p1)  #bernoulli(p1)
                newPrey = (p < p2)  #bernoulli(p2)
                location = (i, j)
                if (newPredator == 1):
                    remainPred -= 1
                    #newPrey = False
                    self.createPredator(location)
                elif newPrey:
                    remainPrey -= 1
                    self.createPrey(location)
                remainTile -= 1
                if (remainPred == 0 and remainPrey == 0):
                    quit = True
                    break
            if quit:
                break
        self.currentOrder = copy.deepcopy(self.nextOrder)
        self.nextOrder = []
        print(self.getNumPredators(), self.getNumPrey())
        return

    '''
    # not called yet; what is self.loc?
    def initializeExactNum(self, freeTiles):
        for i in range(self.mapParams.numStartingPredators):
            if not freeTiles:
                exit()
            newTile = random.choice(freeTiles)
            freeTiles.remove(newTile)
            self.createPredator(self.loc)

        for i in range(self.mapParams.numStartingPrey):
            if not freeTiles:
                exit()
            newTile = random.choice(freeTiles)
            freeTiles.remove(newTile)
            self.createPrey(self.loc)

        self.currentOrder = copy.deepcopy(self.nextOrder)
        self.nextOrder = []
    '''


    def getFreeTiles(self):
        freeTiles = []
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                if not self.map[j][i].hasWater and not self.map[j][i].hasPred and not self.map[j][i].hasWater.hasPrey:
                    freeTiles.append((i, j))

        return freeTiles

    def createPredator(self, loc, param = None):
        # loc is pass in as "x, y"
        if param is None:
            param = self.predatorParams
        x = loc[0]
        y = loc[1]
        newPred = Predator(param, self.sizeX, self.sizeY, x, y,
                           self.animalID)
        self.IDtoAnimal[self.animalID] = newPred
        self.IDtoLoc[self.animalID] = loc
        self.nextOrder.append(self.animalID)
        self.map[y][x].setPredator()

        #set animal_id
        self.map[y][x].animalID = self.animalID

        self.animalID += 1
        self.numAnimals += 1
        self.numPredators += 1

        return

    def createPrey(self, loc, param = None):
        if param is None:
            param = self.preyParams
        x = loc[0]
        y = loc[1]

        newPrey = Prey(param, self.sizeX, self.sizeY, x, y,
                       self.animalID)
        self.IDtoLoc[self.animalID] = loc
        self.IDtoAnimal[self.animalID] = newPrey
        self.nextOrder.append(self.animalID)
        self.map[y][x].setPrey()

        #set animal_id
        self.map[y][x].animalID = self.animalID

        self.animalID += 1
        self.numAnimals += 1
        self.numPrey += 1
        return

    def moveAnimal(self, animalID, loc):
        animal = self.convertIDtoAnimal(animalID)
        tile = self.convertIDtoTile(animalID)
        newTile = self.locToTile(loc)
        if loc == self.IDtoLoc[animalID]:
            return

        #clear old tile
        tile.animal = False
        tile.hasPred = False
        tile.hasPrey = False
        tile.animalID = -1
        tile.occupied = 0
        tile.terrain = "E"

        #update new tile'
        if (newTile.hasPred != 0 or newTile.hasPrey != 0
                or newTile.hasWater != 0):
            #exit(1)
            print('Illegal action: movement onto occupied tile')

        newTile.animalID = animalID
        if animal.isPrey:
            newTile.hasPrey = True
        else:
            newTile.hasPred = True

        newTile.occupied = True
        self.IDtoLoc[animalID] = loc
        return

    def deleteAnimal(self, animalID):
        tile = self.convertIDtoTile(animalID)
        tile.hasPred = 0
        tile.hasPrey = 0
        tile.occupied = False
        tile.animalID = -1
        tile.terrain = "E"
        self.numAnimals = self.numAnimals - 1

        #print("Deleting animal " + str(animal_id))
        #print(self.current_order)
        if animalID in self.currentOrder and self.currentOrder.index(
                animalID) >= self.currentIndex:
            self.currentOrder.remove(animalID)
        #print(self.current_order)

        #print(self.next_order)
        assert (len(self.nextOrder) == len(set(self.nextOrder)))
        if animalID in self.nextOrder:
            self.nextOrder.remove(animalID)
        #print(self.next_order)

        if self.convertIDtoAnimal(animalID).isPrey:
            self.numPrey -= 1
        else:
            self.numPredators -= 1

        self.convertIDtoAnimal(animalID).alive = False

        self.IDtoAnimal.pop(animalID)
        self.IDtoLoc.pop(animalID)

        return

    def getNearbyPlants(self, animalID):
        loc = self.convertIDtoLoc(animalID)
        locsWithFood = []
        # search distance
        searchDist = self.preyParams.foodSearchRadius
        minX = max(0, loc[0] - searchDist)
        maxX = min(self.sizeX, loc[0] + searchDist + 1)
        minY = max(0, loc[1] - searchDist)
        maxY = min(self.sizeY, loc[1] + searchDist + 1)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if self.locToTile((i, j)).hasPlant == True:
                    locsWithFood.append((i, j))

        return locsWithFood

    def getNearbyPredators(self, animalID):
        animal = self.IDtoAnimal[animalID]
        loc = self.convertIDtoLoc(animalID)
        locsWithPredators = []

        if animal.isPrey:
            searchDist = self.preyParams.predatorSearchRadius
        else:
            searchDist = self.predatorParams.reproductiveSearchRadius
        minX = max(0, loc[0] - searchDist)
        maxX = min(self.sizeX, loc[0] + searchDist + 1)
        minY = max(0, loc[1] - searchDist)
        maxY = min(self.sizeY, loc[1] + searchDist + 1)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if self.locToTile((i, j)).hasPred:
                    locsWithPredators.append((i, j))

        return locsWithPredators

    def getNearbyPrey(self, animalID):
        animal = self.IDtoAnimal[animalID]
        loc = self.convertIDtoLoc(animalID)
        locsWithPrey = []

        if animal.isPrey:
            searchDist = self.preyParams.reproductiveSearchRadius
        else:
            searchDist = self.predatorParams.foodSearchRadius

        minX = max(0, loc[0] - searchDist)
        maxX = min(self.sizeX, loc[0] + searchDist + 1)
        minY = max(0, loc[1] - searchDist)
        maxY = min(self.sizeY, loc[1] + searchDist + 1)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if self.locToTile((i, j)).hasPrey:
                    locsWithPrey.append((i, j))

        return locsWithPrey

    def getNearbyWater(self, animalID):
        animal = self.IDtoAnimal[animalID]
        loc = self.convertIDtoLoc(animalID)
        locsWithWater = []
        # search distance
        if animal.isPrey:
            searchDist = self.preyParams.waterSearchRadius
        else:
            searchDist = self.predatorParams.waterSearchRadius

        minX = max(0, loc[0] - searchDist)
        maxX = min(self.sizeX, loc[0] + searchDist + 1)
        minY = max(0, loc[1] - searchDist)
        maxY = min(self.sizeY, loc[1] + searchDist + 1)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if self.locToTile((i, j)).hasWater:
                    locsWithWater.append((i, j))

        return locsWithWater

    def getViableMates(self, animalID):
        animal = self.IDtoAnimal[animalID]
        if not animal.checkIsFertile():
            return []
        loc = self.convertIDtoLoc(animalID)
        locsWithMate = []
        # search distance
        if animal.isPrey:
            searchDist = self.preyParams.reproductiveSearchRadius
        else:
            searchDist = self.predatorParams.reproductiveSearchRadius
        minX = max(0, loc[0] - searchDist)
        maxX = min(self.sizeX, loc[0] + searchDist + 1)
        minY = max(0, loc[1] - searchDist)
        maxY = min(self.sizeY, loc[1] + searchDist + 1)
        for i in range(minX, maxX):
            for j in range(minY, maxY):
                if self.map[j][i].isAnimal():
                    other = self.IDtoAnimal[self.map[j][i].animalID]
                    if other.checkIsFertile() and (
                            other.isPrey == animal.isPrey
                    ) and other.isFemale != animal.isFemale:
                        locsWithMate.append((i, j))
        return locsWithMate

    def getTemp(self):
        return self.currTemp

    def getNextAnimal(self):
        if self.currentIndex >= len(self.currentOrder):
            self.currentIndex = 0
            self.currentOrder = copy.deepcopy(self.nextOrder)
            self.nextOrder = []
            return None

        self.currentIndex += 1
        return self.currentOrder[self.currentIndex - 1]

    def getNumAnimals(self):
        return self.numAnimals

    def getNumPredators(self):
        return self.numPredators

    def getNumPrey(self):
        return self.numPrey

    def createGraph(self, deathCounts, predatorAverageMaxFood, preyAverageMaxFood):
        xAxis = []
        for i in range(0, 101):
            if (i % 2 == 0):
                xAxis.append(i)
        
        # POPULATION COUNTS
        plt.subplot(2, 2, 1)
        plt.plot(self.predatorCount, label="Predator Count")
        plt.plot(self.preyCount, label="Prey Count")
        plt.legend(loc="upper left")
        plt.title("Population Distribution")
        plt.xlabel("Time")
        plt.ylabel("Population")
        #plt.ylim([0,100])

        # AVERAGE MAX FOOD
        plt.subplot(2, 2, 3)
        plt.plot(predatorAverageMaxFood, label="Predator")
        plt.plot(preyAverageMaxFood, label="Prey")
        plt.legend(loc="upper left")
        plt.title("Average Max Food")
        plt.xlabel("Time")
        plt.ylabel("Population")

        # PREDATOR CAUSE OF DEATH
        plt.subplot(2, 2, 2)
        plt.plot([x[3] for x in deathCounts], label="Hunger")
        plt.plot([x[4] for x in deathCounts], label="Thirst")
        plt.legend(loc="upper left")
        plt.title("Predator Causes of Death")
        plt.xlabel("Time")
        plt.ylabel("Population")
        
        # PREY CAUSE OF DEATH
        plt.subplot(2, 2, 4)
        plt.plot(np.array(deathCounts)[:, 0], label="Hunger")
        plt.plot(np.array(deathCounts)[:, 1], label="Thirst")
        plt.plot(np.array(deathCounts)[:, 2], label="Eaten")
        plt.legend(loc="upper left")
        plt.title("Prey Causes of Death")
        plt.xlabel("Time")
        plt.ylabel("Population")

        plt.subplots_adjust(wspace=0.2,hspace=0.4)
        plt.show()

        # after that: back to varying reproduction stuff


    def getAverageMaxFood(self):
        return(sum(self.IDtoAnimal[id].maxFood for id in self.currentOrder)/max(1, self.numAnimals))

    def getAverageMaxWater(self):
        return(sum(self.IDtoAnimal[id].maxWater for id in self.currentOrder)/max(1, self.numAnimals))
    
    # Average Prey Values
    def getPreyAverageMaxFood(self):
        return(sum(self.IDtoAnimal[id].maxFood for id in self.currentOrder if self.IDtoAnimal[id].isPrey)/max(1, self.numPrey))
    
    def getPreyAverageMaxWater(self):
        return(sum(self.IDtoAnimal[id].maxWater for id in self.currentOrder if self.IDtoAnimal[id].isPrey)/max(1, self.numPrey))
    
    # Average Predator Values
    def getPredatorAverageMaxFood(self):
        return(sum(self.IDtoAnimal[id].maxFood for id in self.currentOrder if not self.IDtoAnimal[id].isPrey)/max(1, self.numPredators))

    def getPredatorAverageMaxWater(self):
        return(sum(self.IDtoAnimal[id].maxWater for id in self.currentOrder if not self.IDtoAnimal[id].isPrey)/max(1, self.numPredators))