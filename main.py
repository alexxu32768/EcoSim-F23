from Simulation import Simulation
from AnimalParams import SimulationParams, MapParams, AnimalParams

simulationParams = SimulationParams()
simulationParams.simulationLength = 200
simulationParams.simulationSpeed = 200  #delay in ms

mapParams = MapParams()
mapParams.sizeX = 50
mapParams.sizeY = 30
mapParams.percentWaterCoverage = 30
mapParams.numStartingPredators = 20
mapParams.numStartingPrey = 30
mapParams.temp = 70

predatorParams = AnimalParams()
predatorParams.maxFood = 100
predatorParams.maxWater = 100
predatorParams.minReproductiveAge = 5
predatorParams.reproductiveDelay = 3
predatorParams.waterSearchRadius = 2
predatorParams.foodSearchRadius = 3
predatorParams.reproductiveSearchRadius = 4
predatorParams.hungerIncreasePercentage = 0.03
predatorParams.thirstIncreasePercentage = 0.03
predatorParams.hungerDecreasePercentage = 0.25
predatorParams.thirstDecreasePercentage = 0.25
predatorParams.minReproductiveHunger = .50
predatorParams.minReproductiveThirst = .50

preyParams = AnimalParams()
preyParams.maxFood = 100
preyParams.maxWater = 100
preyParams.minReproductiveAge = 5
preyParams.reproductiveDelay = 4
preyParams.waterSearchRadius = 2
preyParams.foodSearchRadius = 2
preyParams.predatorSearchRadius = 3
preyParams.reproductiveSearchRadius = 4
preyParams.hungerIncreasePercentage = 0.03
preyParams.thirstIncreasePercentage = 0.03
preyParams.hungerDecreasePercentage = 0.25
preyParams.thirstDecreasePercentage = 0.25
preyParams.minReprocutiveHunger = 0.50
preyParams.minReproductiveThirst = 0.50

simulation = Simulation(simulationParams, mapParams, predatorParams,
                        preyParams)
simulation.runSimulation()
