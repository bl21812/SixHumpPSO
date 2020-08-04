from Swarm import Swarm

swarm1 = Swarm(100, 2.05, 2.05)
swarm1.runConstriction()
print(swarm1.bestSol)
print(swarm1.bestSolValue)
