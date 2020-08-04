import math
import random

class Particle:

    def __init__(self, pos, vel, w):
        self.pos = pos
        self.vel = vel
        self.initW = w  # initial inertia constant
        self.w = w  # inertia constant
        self.pbestVal = self.evalSelf()  # value of best solution
        self.pbest = pos  # best solution
        self.neighbours = [] # matrix of neighbours (social neighbours)
        self.nbest = self.pbest
        self.nbestVal = self.pbestVal

    # Returns vector [x, y, val] of neighbourhood best sol
    def nbestFind(self):
        temp = self.pbest
        tempVal = self.pbestVal
        for neighbour in self.neighbours:
            if neighbour.pbestVal < tempVal:
                tempVal = neighbour.pbestVal
                temp = neighbour.pbest
        return [temp, tempVal]

    # Updates velocity with constriction factor method (no return)
    def velUpdateConstriction(self, c1, c2, k, gbest):
        r1 = random.random()
        r2 = random.random()
        self.vel[0] = k * math.floor(self.vel[0] + c1 * r1 * (self.pbest[0] - self.pos[0]) + c2 * r2 * (gbest[0] - self.pos[0]))

        r1 = random.random()
        r2 = random.random()
        self.vel[1] = k * math.floor(self.vel[1] + c1 * r1 * (self.pbest[1] - self.pos[1]) + c2 * r2 * (gbest[1] - self.pos[1]))

    def velUpdateInertia(self, c1, c2, wmax, wmin, iter, iterMax):
        self.w = wmax - (wmax - wmin) * iter / iterMax

        r1 = random.random()
        r2 = random.random()
        self.vel[0] = self.w * self.vel[0] + c1 * r1 * (self.pbest[0] - self.pos[0]) + c2 * r2 * (self.nbest[0] - self.pos[0])

        r1 = random.random()
        r2 = random.random()
        self.vel[1] = self.w * self.vel[1] + c1 * r1 * (self.pbest[1] - self.pos[1]) + c2 * r2 * (self.nbest[1] - self.pos[1])


    def posUpdate(self):
        self.pos[0] += self.vel[0]
        if self.pos[0] < -5:
            self.pos[0] = -5
        elif self.pos[0] > 5:
            self.pos[0] = 5
        self.pos[1] += self.vel[1]
        if self.pos[1] < -5:
            self.pos[1] = -5
        elif self.pos[1] > 5:
            self.pos[1] = 5

    # Updates neighbourhood best, based on caller's state
    # DONT NEED THIS
    def nbestUpdate(self):
        neighbourBest = self.nbestFind()
        self.nbest = [neighbourBest[0][0], neighbourBest[0][1]]
        self.nbestVal = neighbourBest[1]

    # Updates nbest for all neighbours
    def nbestUpdateNeighbours(self):
        for neighbour in self.neighbours:
            if self.pbestVal < neighbour.nbestVal:
                neighbour.nbestVal = self.pbestVal
                neighbour.nbest = self.pbest

    def inerUpdate(self):
        print()

    # Evaluate value of particle's position
    def evalSelf(self):
        x = self.pos[0]
        y = self.pos[1]
        temp1 = (4 - 2.1 * pow(x, 2) + pow(x, 4) / 3) * pow(x, 2)
        temp2 = x * y
        temp3 = (-4 + 4 * pow(y, 2)) * pow(y, 2)
        return temp1 + temp2 + temp3

    def __str__(self):
        return "Position: " + str(self.pos[0]) + ', ' + str(self.pos[1]) + '; ' + "pBest: " + str(self.pbest[0]) + ', ' + str(self.pbest[1]) + ', Value: ' + str(self.pbestVal) + "; " + "nBest: " + str(self.nbest[0]) + ', ' + str(self.nbest[1]) + ", Value: " + str(self.nbestVal) + '\n'
