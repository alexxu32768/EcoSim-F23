from Animal import Animal
import random
from random import randrange
from SensoryRange import SensoryRange
from Action import DieAction
from Action import EatAction
from Action import MoveAction
from Action import ReproduceAction
from Action import DrinkAction
from AnimalParams import SimulationParams, MapParams, AnimalParams


class Prey(Animal):

    def __init__(self,
                 preyParams,
                 xmax,
                 ymax,
                 positionX=None,
                 positionY=None,
                 animalID=None):

        self.maxFood = preyParams.maxFood
        self.currFood = self.maxFood * .25
        self.maxWater = preyParams.maxWater
        self.currWater = self.maxWater * .75

        self.minReproductiveAge = preyParams.minReproductiveAge
        self.reproductiveDelay = preyParams.reproductiveDelay
        self.waterSearchRadius = preyParams.waterSearchRadius
        self.foodSearchRadius = preyParams.foodSearchRadius
        self.reproductiveSearchRadius = preyParams.reproductiveSearchRadius
        self.hungerIncreaseAmount = preyParams.hungerIncreaseAmount
        self.thirstIncreaseAmount = preyParams.thirstIncreaseAmount
        self.hungerDecreaseAmount = preyParams.hungerDecreaseAmount
        self.thirstDecreaseAmount = preyParams.thirstDecreaseAmount

        self.isFemale = random.choice([0, 1])
        self.isPrey = 1
        self.isFertile = 0
        self.animalID = animalID
        if positionX == None:
            self.setRandomLocation()
        else:
            self.positionX = positionX
            self.positionY = positionY
        self.alive = 1
        self.xmax = xmax
        self.ymax = ymax
        self.age = 0
        self.reprDelay = 0
        super().__init__(preyParams)

    def eatPlant(self, surroundings):
        actionList = []
        # nearbyFood is coordinate of nearest plant
        nearbyPlants = surroundings.getNearbyPlants()

        if nearbyPlants == []:
            # returns None if cannot eat plant
            return actionList
        for loc in nearbyPlants:
            #eat plant if location is found adjacent to the animal
            if (max(abs(loc[0] - self.positionX), abs(loc[1] - self.positionY))
                    <= 1):
                # not capped rn, but animals only eat when they are sufficiently hungry
                self.currFood += self.hungerDecreaseAmount
                # returns the coordinate of the water
                eatAction = EatAction()
                eatAction.setFoodType("plant")
                eatAction.setFoodLocation(loc)
                actionList.append(eatAction)
                return actionList

        #move towards the nearest food location
        #TODO: move towards NEAREST plant, not just the first plant observed
        invalidLocs = surroundings.getNearbyPrey(
        ) + surroundings.getNearbyPredators() + surroundings.getNearbyWater()

        moveaction = self.genMoveAction(nearbyPlants[0], invalidLocs)
        if moveaction is not None:
            actionList.append(moveaction)
        return actionList

    def reproduce(self, surroundings):
        nearbyMates = surroundings.getNearbyMates()
        for i in nearbyMates:

            # can mate: opposite genders, both fertile, other didnt move
            # neither animal moves
            # animal is reproducing
            actionList = []
            reproduceAction = ReproduceAction()
            reproduceAction.setAnimalType("prey")

            openTiles = self.getOpenTiles(surroundings)
            if not openTiles:
                return []
            reproduceAction.setBirthLocation(random.choice(openTiles))

            reproduceAction.setPartnerLocation(i)
            reproduceAction.setSelfLocation((self.positionX, self.positionY))

            actionList.append(reproduceAction)

            self.reprDelay = 0
            return actionList

    def preyReact(self, animalSr):
        #print(self.currFood)
        # make use_resource function: use food and water (small amts) for any action; call it here

        self.currWater -= self.thirstIncreaseAmount
        self.currFood -= self.hungerIncreaseAmount
        currentActionList = []

        self.checkState()  #check if it is alive
        #self.tempReact(animal_sr)
        if self.alive == 0:
            dieAction = DieAction()
            dieAction.setCause("thirst" if self.currFood > 0 else "hunger")
            currentActionList.append(dieAction)
            return currentActionList
            # tell sim to delete self

        if self.currFood < (0.75 * self.maxFood):
            actionList = self.eatPlant(
                animalSr
            )  #should be a list with coords of plant and 2, or None if nothing was eaten

            if actionList:
                return actionList

        if self.currWater < (.75 * self.maxWater):
            actionList = self.waterReact(animalSr)
            if actionList:
                return actionList

        if self.checkIsFertile():
            actionList = self.reproduce(animalSr)

            if actionList:
                return actionList

        # if nothing happens, will randomly move

        moveAction = MoveAction()
        currLocation = (self.positionX, self.positionY)

        endLocation = self.randomMove(animalSr)

        if endLocation == None:
            return []

        moveAction.setstartLocation(currLocation)
        moveAction.setendLocation(endLocation)
        currentActionList.append(moveAction)

        return currentActionList
