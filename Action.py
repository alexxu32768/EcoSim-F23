import random 

class Action:

    def __init__(self, actionType=None):
        self.type = actionType

    def setActionType(self, actionType):
        self.type = actionType


class EatAction(Action):

    def __init__(self):
        self.type = "eat"
        self.foodType = None
        self.foodLocation = (0, 0)
        self.animalID = None

    def setFoodLocation(self, foodLocation):
        self.foodLocation = foodLocation

    def setFoodType(self, foodType):
        self.foodType = foodType

    def setFoodID(self, animalID):
        set.animalID = animalID

    def getFoodType(self):
        return self.foodType

    def getFoodLocation(self):
        return self.foodLocation

    def getFoodID(self, animalID):
        return set.animalID


class MoveAction(Action):

    def __init__(self):
        self.type = "move"
        self.startLocation = (0, 0)
        self.endLocation = (0, 0)

    def setstartLocation(self, startLocation):
        self.startLocation = startLocation

    def setendLocation(self, endLocation):
        self.endLocation = endLocation

    def getstartLocat(self):
        return self.startLocation

    def getendLocation(self):
        return self.endLocation


class ReproduceAction(Action):

    def __init__(self):
        self.type = "reproduce"
        self.birthLocation = (0, 0)
        self.selfLocation = (0, 0)
        self.partnerLocation = (0, 0)
        self.animalType = None
        self.animalParams = None # parameters of parent(s)

    def setBirthLocation(self, birthLocation):
        self.birthLocation = birthLocation

    def setAnimalType(self, animalType):
        self.animalType = animalType
    
    def setSelfLocation(self, selfLocation):
        self.selfLocation = selfLocation

    def setPartnerLocation(self, partnerLocation):
        self.partnerLocation = partnerLocation

    def getBirthLocation(self):
        return self.birthLocation

    def getAnimalType(self):
        return self.animalType

    def getPartnerLocation(self):
        return self.partnerLocation


class DrinkAction(Action):

    def __init__(self):
        self.type = "drink"


class DieAction(Action):

    def __init__(self):
        self.type = "die"
        self.cause = None # hunger, thirst; handle eaten separately

    def setCause(self, dieCause):
        self.cause = dieCause
