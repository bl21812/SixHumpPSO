import math
from Particle import Particle
import random
import numpy

class Swarm:

    # Initialize swarm as square matrix (will truncate if population not perfect square)
    def __init__(self, popSize, c1, c2):
        length = int(math.sqrt(popSize))
        self.pop = numpy.empty([length, length], dtype=Particle)
        self.c1 = c1
        self.c2 = c2
        phi = c1 + c2
        self.k = 2 / abs(2 - phi - math.sqrt(pow(phi, 2) - 4 * phi))

        self.bestPerGen = []  # Stores value of best sol per generation
        self.bestSol = [0, 0]
        self.bestSolValue = 99999
        self.averagePerGen = []  # Stores average fitness per generation

        for i in range(length): # init pop
            for j in range(length):
                tempX = random.random() * 10.0 - 5.0
                tempY = random.random() * 10.0 - 5.0
                initW = 0.792
                self.pop[i][j] = Particle([tempX, tempY], [0, 0], initW)
        for i in range(length): # init neighbours for pop
            for j in range(length):
                self.setNeighbours(i, j, self.pop[i][j])
        # Set neighbourhood best values
        for i in range(len(self.pop)):
            for j in range(len(self.pop)):
                self.pop[i][j].nbestUpdate()

    # Set neighbours of a particle
    def setNeighbours(self, i, j, ind):
        if i > 0:
            ind.neighbours.append(self.pop[i-1][j])
        if i < (len(self.pop) - 1):
            ind.neighbours.append(self.pop[i+1][j])
        if j > 0:
            ind.neighbours.append(self.pop[i][j-1])
        if j < (len(self.pop) - 1):
            ind.neighbours.append(self.pop[i][j+1])

    # Returns best solution in neighbourhood given indices of individual in pop matrix
    def neighbourBest(self, i, j):
        print()

    # Inertia weight
    def runInerWeight(self):
        # Run search
        iter = 0
        maxW = 1.0
        minW = 0.1

        while iter < 200:  # set max of 200 iterations
            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            gbest = [0, 0]
            for i in range(len(self.pop)):
                for j in range(len(self.pop)):
                    curr = self.pop[i][j]
                    curr.velUpdateInertia(self.c1, self.c2, maxW, minW, iter, 200)  # Velocity update
                    curr.posUpdate()  # Position update
                    # Update neighbourhood best - for this particle and all others in its neighbourhood
                    curr.nbestUpdate()
                    curr.nbestUpdateNeighbours()
                    # Set best in generation
                    tempVal = curr.evalSelf()
                    if tempVal < bestGenVal:
                        bestGenVal = tempVal
                        bestGen = curr.pos
                    fitnessSum += tempVal  # for average fitness in gen
            # Change global best if applicable and set best in gen
            if bestGenVal < self.bestSolValue:
                self.bestSol = bestGen
                self.bestSolValue = bestGenVal
            self.bestPerGen.append(bestGenVal)
            self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))
            iter += 1

    # Constriction factor
    def runConstriction(self):
        iter = 0
        while iter < 200:  # set max of 200 iterations
            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            gbest = [0, 0]
            for i in range(len(self.pop)):
                for j in range(len(self.pop)):
                    gbest = self.gbestFind()  # Get global best for velocity update
                    curr = self.pop[i][j]
                    curr.velUpdateConstriction(self.c1, self.c2, self.k, gbest)  # Velocity update
                    curr.posUpdate()  # Position update
                    # Update neighbourhood best - for this particle and all others in its neighbourhood
                    curr.nbestUpdate()
                    curr.nbestUpdateNeighbours()
                    # Set best in generation
                    tempVal = curr.evalSelf()
                    if tempVal < bestGenVal:
                        bestGenVal = tempVal
                        bestGen = curr.pos
                    fitnessSum += tempVal  # for average fitness in gen
            # Change global best if applicable and set best in gen
            if bestGenVal < self.bestSolValue:
                self.bestSol = bestGen
                self.bestSolValue = bestGenVal
            self.bestPerGen.append(bestGenVal)
            self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))
            iter += 1


    # GCPSO
    def runGC(self):
        iter = 0
        while iter < 500:  # set max of 500 iterations
            for i in range(len(self.pop)):
                for j in range(len(self.pop)):
                    # Update velocity, then position (and particle PB)
                    # Update neighbourhood best - for this particle and all others in its neighbourhood
                    print()

   # Returns global best solution (not the value with it)
    def gbestFind(self):
        tempBestVal = 99999
        tempBest = [0, 0]
        for i in range(len(self.pop)):
            for j in range(len(self.pop)):
                tempVal = self.pop[i][j].evalSelf()
                if tempVal < tempBestVal:
                    tempBest = self.pop[i][j].pos
        return tempBest

    def __str__(self):
        for i in range(len(self.pop)):
            for j in range(len(self.pop)):
                print(self.pop[i][j])
