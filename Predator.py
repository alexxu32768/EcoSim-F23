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


class Predator(Animal):

    def __init__(self,
                 predatorParams,
                 xmax,
                 ymax,
                 positionX=None,
                 positionY=None,
                 animalID=None):

        # hardcoded percentage for initial curr
        self.maxFood = predatorParams.maxFood
        self.currFood = self.maxFood * .25
        self.maxWater = predatorParams.maxWater
        self.currWater = self.maxWater * .75

        self.minReproductiveAge = predatorParams.minReproductiveAge
        self.reproductiveDelay = predatorParams.reproductiveDelay
        self.waterSearchRadius = predatorParams.waterSearchRadius
        self.foodSearchRadius = predatorParams.foodSearchRadius
        self.reproductiveSearchRadius = predatorParams.reproductiveSearchRadius
        self.hungerIncreaseAmount = predatorParams.hungerIncreaseAmount
        self.thirstIncreaseAmount = predatorParams.thirstIncreaseAmount
        self.hungerDecreaseAmount = predatorParams.hungerDecreaseAmount
        self.thirstDecreaseAmount = predatorParams.thirstDecreaseAmount

        self.isFemale = random.choice([0, 1])
        self.isPrey = 0
        self.isFertile = 0
        self.animalId = animalID
        if positionX == None or positionY == None:
            self.setRandomLocation()
        else:
            self.positionX = positionX
            self.positionY = positionY
        self.alive = 1
        self.xmax = xmax
        self.ymax = ymax
        self.age = 0
        self.reprDelay = 0

        super().__init__(predatorParams)

    def eatPrey(self, surroundings):
        # list of action the animal want to take
        actionList = []
        # nearbyFood is coordinate of nearest plant
        nearbyPrey = surroundings.getNearbyPrey()

        if nearbyPrey == []:
            # returns None if cannot eat plant
            return actionList
        for loc in nearbyPrey:
            #eat plant if location is found adjacent to the animal
            if (max(abs(loc[0] - self.positionX), abs(loc[1] - self.positionY))
                    <= 1):
                self.currFood += self.hungerDecreaseAmount
                # returns the coordinate of the water
                eatAction = EatAction()
                eatAction.setFoodType("animal")
                eatAction.setFoodLocation(loc)
                actionList.append(eatAction)
                return actionList

        #move towards the nearest food location
        invalidLocs = surroundings.getNearbyPrey(
        ) + surroundings.getNearbyPredators() + surroundings.getNearbyWater()

        moveaction = self.genMoveAction(nearbyPrey[0], invalidLocs)
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
            reproduceAction.setAnimalType("pred")

            openTiles = self.getOpenTiles(surroundings)
            if not openTiles:
                return []
            reproduceAction.setBirthLocation(random.choice(openTiles))
            reproduceAction.setPartnerLocation(i)

            actionList.append(reproduceAction)

            self.reprDelay = 0
            return actionList

    # action is deterministic, thresholds are also hardcoded
    def predReact(self, animalSr):
        # make use_resource function: use food and water (small amts) for any action; call it here

        # food and water will decrease by a constant amount no matter what
        self.currWater -= self.thirstIncreaseAmount
        self.currFood -= self.hungerIncreaseAmount
        currentActionList = []

        self.checkState()  #check if it is alive
        # self.tempReact()
        if not self.alive:
            dieAction = DieAction()
            currentActionList.append(dieAction)
            return currentActionList
            # tell sim to delete self

        if self.currFood < (0.60 * self.maxFood):
            actionList = self.eatPrey(
                animalSr
            )  #should be a list with coords and 1 or 2 depending on pred or prey eaten, or None if nothing was eaten
            if actionList:
                return actionList

        if self.currWater < (.60 * self.maxWater):
            actionList = self.waterReact(animalSr)

            if actionList:
                return actionList

        if self.checkIsFertile():
            actionList = self.reproduce(animalSr)

            if actionList:
                return actionList

        # no action taken, so animal just moves
        moveAction = MoveAction()
        currLocation = (self.positionX, self.positionY)
        #self.random_move()

        invalidLocs = animalSr.getNearbyPrey() + animalSr.getNearbyPredators(
        ) + animalSr.getNearbyWater()
        self.randomMove(animalSr)

        endLocation = (self.positionX, self.positionY)
        if endLocation not in invalidLocs:
            moveAction.setstartLocation(currLocation)
            moveAction.setendLocation(endLocation)
            currentActionList.append(moveAction)

        #send out desired action to sim
        return currentActionList
