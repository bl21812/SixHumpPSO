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
        self.phi = c1 + c2

        self.bestPerGen = []  # Stores value of best sol per generation
        self.bestSol = [0, 0]
        self.bestSolValue = 99999
        self.averagePerGen = []  # Stores average fitness per generation

        self.iter = 0

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

    def runBasic(self):
        # Run search
        self.iter = 0

        while self.iter < 100:  # set max of 100 iterations
            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            currGenVals = []  # Fitnesses for current gen
            for i in range(len(self.pop)):
                for j in range(len(self.pop)):
                    curr = self.pop[i][j]
                    curr.velUpdateBasic(self.c1, self.c2)  # Velocity update
                    curr.posUpdate()  # Position update
                    # Update neighbourhood best - for this particle and all others in its neighbourhood
                    curr.nbestUpdate()
                    curr.nbestUpdateNeighbours()
                    # Set best in generation
                    tempVal = curr.evalSelf()
                    if tempVal < bestGenVal:
                      bestGenVal = tempVal
                      bestGen = curr.pos
                      currGenVals.append(tempVal)
                    fitnessSum += tempVal  # for average fitness in gen
            
            # Add to best per gen
            if len(self.bestPerGen):
              if min(currGenVals) < self.bestPerGen[-1]:
                self.bestPerGen.append(numpy.min(currGenVals))
              else:
                self.bestPerGen.append(numpy.min(self.bestPerGen))
            else:
              self.bestPerGen.append(numpy.min(currGenVals))

            # Change global best if applicable and set best in gen
            if bestGenVal < self.bestSolValue:
                self.bestSol = bestGen
                self.bestSolValue = bestGenVal

            # Append to average per gen
            self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))

            self.iter += 1

    # Inertia weight
    def runInerWeight(self):
        # Run search
        self.iter = 0
        maxW = 1.0
        minW = 0.1
        self.k = 2 / abs(2 - self.phi - math.sqrt(pow(self.phi, 2) - 4 * self.phi))

        while self.iter < 100:  # set max of 100 iterations
            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            currGenVals = []  # Fitnesses for current gen
            for i in range(len(self.pop)):
                for j in range(len(self.pop)):
                    curr = self.pop[i][j]
                    curr.velUpdateInertia(self.c1, self.c2, maxW, minW, self.iter, 200)  # Velocity update
                    curr.posUpdate()  # Position update
                    # Update neighbourhood best - for this particle and all others in its neighbourhood
                    curr.nbestUpdate()
                    curr.nbestUpdateNeighbours()
                    # Set best in generation
                    tempVal = curr.evalSelf()
                    if tempVal < bestGenVal:
                        bestGenVal = tempVal
                        bestGen = curr.pos
                        currGenVals.append(tempVal)
                    fitnessSum += tempVal  # for average fitness in gen
                    
            # Add to best per gen
            if len(self.bestPerGen):
              if min(currGenVals) < self.bestPerGen[-1]:
                self.bestPerGen.append(numpy.min(currGenVals))
              else:
                self.bestPerGen.append(numpy.min(self.bestPerGen))
            else:
              self.bestPerGen.append(numpy.min(currGenVals))

            # Change global best if applicable and set best in gen
            if bestGenVal < self.bestSolValue:
                self.bestSol = bestGen
                self.bestSolValue = bestGenVal

            # Append to average per gen
            self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))

            self.iter += 1

    # Constriction factor
    def runConstriction(self):
        self.iter = 0
        self.k = 2 / abs(2 - self.phi - math.sqrt(pow(self.phi, 2) - 4 * self.phi))
        while self.iter < 100:  # set max of 100 iterations
            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            gbest = [0, 0]
            currGenVals = []  # Fitnesses for current gen
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
                        currGenVals.append(tempVal)
                    fitnessSum += tempVal  # for average fitness in gen
                    
            # Add to best per gen
            if len(self.bestPerGen):
              if min(currGenVals) < self.bestPerGen[-1]:
                self.bestPerGen.append(numpy.min(currGenVals))
              else:
                self.bestPerGen.append(numpy.min(self.bestPerGen))
            else:
              self.bestPerGen.append(numpy.min(currGenVals))

            # Change global best if applicable and set best in gen
            if bestGenVal < self.bestSolValue:
                self.bestSol = bestGen
                self.bestSolValue = bestGenVal

            # Append to average per gen
            self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))

            self.iter += 1


    # GCPSO
    def runGC(self):
        self.iter = 0
        currBestVal = 99999
        currBest = self.pop[0][0]
        maxW = 1.0
        minW = 0.1
        while self.iter < 100:  # set max of 100 iterations

            # Reset appropriate values
            prevBestVal = currBestVal
            prevBest = currBest
            currBestVal = 99999
            currBest = self.pop[0][0]

            bestGen = [0, 0]  # temp for best in a gen
            bestGenVal = 99999  # value for the above
            fitnessSum = 0.0
            currGenVals = []  # Fitnesses for current gen

            if self.iter == 0:  # first iteration - this is the SAME as inertia weight, since no successes/failures

                # For initial population - set the 'previous best' values for the next iteration to compare to
                for i in range(len(self.pop)):
                    for j in range(len(self.pop)):
                        curr = self.pop[i][j]
                        tempVal = curr.evalSelf()
                        if tempVal < currBestVal:
                            currBestVal = tempVal
                            currBest = curr

                # Update velocities, positions by inertia weight
                for i in range(len(self.pop)):
                    for j in range(len(self.pop)):
                        curr = self.pop[i][j]
                        curr.velUpdateInertia(self.c1, self.c2, maxW, minW, self.iter, 200)  # Velocity update
                        curr.posUpdate()  # Position update
                        # Update neighbourhood best - for this particle and all others in its neighbourhood
                        curr.nbestUpdate()
                        curr.nbestUpdateNeighbours()
                        # Set best in generation
                        tempVal = curr.evalSelf()
                        if tempVal < bestGenVal:
                            bestGenVal = tempVal
                            bestGen = curr.pos
                            currGenVals.append(tempVal)
                        fitnessSum += tempVal  # for average fitness in gen

                # Add to best per gen
                if len(self.bestPerGen):
                  if min(currGenVals) < self.bestPerGen[-1]:
                    self.bestPerGen.append(numpy.min(currGenVals))
                  else:
                    self.bestPerGen.append(numpy.min(self.bestPerGen))
                else:
                  self.bestPerGen.append(numpy.min(currGenVals))

                # Change global best if applicable and set best in gen
                if bestGenVal < self.bestSolValue:
                    self.bestSol = bestGen
                    self.bestSolValue = bestGenVal

                # Append to average per gen
                self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))

                self.iter += 1

            else:  # all non-first iterations

                # Determine the current best
                for i in range(len(self.pop)):
                    for j in range(len(self.pop)):
                        curr = self.pop[i][j]
                        tempVal = curr.evalSelf()
                        if tempVal < currBestVal:
                            currBestVal = tempVal
                            currBest = curr

                # Compare to previous best, and update appropriate success/failure counter
                if currBest is prevBest:
                    if currBestVal == prevBestVal:  # increase failure count if best was stagnant
                        currBest.successes = 0
                        currBest.failures += 1
                    else:  # increase success count if the prev best particle is still the best, but has a dif position
                        currBest.failures = 0
                        currBest.successes += 1
                else:  # Reset counts for previous best if the best particle changed
                    prevBest.successes = 0
                    prevBest.failures = 0

                # Update velocities, positions by GCPSO for best particle, and inertia weight for the rest
                for i in range(len(self.pop)):
                    for j in range(len(self.pop)):
                        curr = self.pop[i][j]
                        if curr is currBest:  # GCPSO update for current best particle
                            oldVel = curr.velUpdateGCPSO(self.bestSol)
                            curr.posUpdateGCPSO(self.bestSol, oldVel)
                        else:  # Inertia weight update for all other particles
                            curr.velUpdateInertia(self.c1, self.c2, maxW, minW, self.iter, 200)  # Velocity update
                            curr.posUpdate()  # Position update
                        # Update neighbourhood best - for this particle and all others in its neighbourhood
                        curr.nbestUpdate()
                        curr.nbestUpdateNeighbours()
                        # Set best in generation
                        tempVal = curr.evalSelf()
                        if tempVal < bestGenVal:
                            bestGenVal = tempVal
                            bestGen = curr.pos
                            currGenVals.append(tempVal)
                        fitnessSum += tempVal  # for average fitness in gen

                # Add to best per gen
                if len(self.bestPerGen):
                  if min(currGenVals) < self.bestPerGen[-1]:
                    self.bestPerGen.append(numpy.min(currGenVals))
                  else:
                    self.bestPerGen.append(numpy.min(self.bestPerGen))
                else:
                  self.bestPerGen.append(numpy.min(currGenVals))

                # Change global best if applicable and set best in gen
                if bestGenVal < self.bestSolValue:
                    self.bestSol = bestGen
                    self.bestSolValue = bestGenVal

                # Append to average per gen
                self.averagePerGen.append(fitnessSum / pow(len(self.pop), 2))

                self.iter += 1

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
