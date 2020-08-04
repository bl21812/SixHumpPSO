from Swarm import Swarm
import matplotlib.pyplot as plt

c1 = 2.05
c2 = 2.05

swarm1 = Swarm(64, c1, c2)
swarm2 = Swarm(64, c1, c2)
swarm3 = Swarm(64, c1, c2)

swarm1.runConstriction()
swarm2.runConstriction()
swarm3.runConstriction()

print(swarm1.bestSolValue, swarm1.bestSol)
print(swarm2.bestSolValue, swarm2.bestSol)
print(swarm3.bestSolValue, swarm3.bestSol)

gens = [i for i in range(1, 201)]

fig, (a1, a2) = plt.subplots(2)
a1.plot(gens, swarm1.bestPerGen, 'r-', gens, swarm2.bestPerGen, 'g-', gens, swarm3.bestPerGen, 'b-')
a2.plot(gens, swarm1.averagePerGen, 'r-', gens, swarm2.averagePerGen, 'g-', gens, swarm3.averagePerGen, 'b-')

#plt.plot(gens, swarm1.bestPerGen, 'r-', gens, swarm2.bestPerGen, 'g-', gens, swarm3.bestPerGen, 'b-')
#a1.ylabel("Fitness of best particle in generation")
#a2.ylabel("Average fitness of population")
plt.xlabel("Generation #")
#plt.title("Best solution per generation vs. Generation #")
plt.show()

