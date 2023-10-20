from Simulation import Simulation
from AnimalParams import SimulationParams, MapParams, AnimalParams

simulationParams = SimulationParams()
simulationParams.simulationLength = 1000
simulationParams.simulationSpeed = 20  #delay in ms

mapParams = MapParams()
mapParams.sizeX = 80
mapParams.sizeY = 50
mapParams.percentWaterCoverage = 30
mapParams.numStartingPredators = 80
mapParams.numStartingPrey = 200
mapParams.temp = 70

predatorParams = AnimalParams()
predatorParams.maxFood = 100
predatorParams.maxWater = 100
predatorParams.minReproductiveAge = 15
predatorParams.reproductiveDelay = 15
predatorParams.waterSearchRadius = 5
predatorParams.foodSearchRadius = 5
predatorParams.reproductiveSearchRadius = 30
predatorParams.hungerIncreaseAmount = 3
predatorParams.thirstIncreaseAmount = 3
predatorParams.hungerDecreaseAmount = 50
predatorParams.thirstDecreaseAmount = 50
predatorParams.minReproductiveHunger = 50
predatorParams.minReproductiveThirst = 50

preyParams = AnimalParams()
preyParams.maxFood = 100
preyParams.maxWater = 100
preyParams.minReproductiveAge = 10
preyParams.reproductiveDelay = 10
preyParams.waterSearchRadius = 15
preyParams.foodSearchRadius = 15
preyParams.reproductiveSearchRadius = 15
preyParams.predatorSearchRadius = 6
preyParams.hungerIncreaseAmount = 3
preyParams.thirstIncreaseAmount = 3
preyParams.hungerDecreaseAmount = 50
preyParams.thirstDecreaseAmount = 50
preyParams.minReproductiveHunger = 50
preyParams.minReproductiveThirst = 50

simulation = Simulation(simulationParams, mapParams, predatorParams,
                        preyParams)
simulation.runSimulation()
