from Swarm import Swarm
import matplotlib.pyplot as plt

c1 = 1.4944
c2 = 1.4944
popSize = 64

swarm1 = Swarm(popSize, c1, c2)
swarm2 = Swarm(popSize, c1, c2)
swarm3 = Swarm(popSize, c1, c2)

swarm1.runBasic()
swarm2.runBasic()
swarm3.runBasic()

print(swarm1.bestSolValue, swarm1.bestSol)
print(swarm2.bestSolValue, swarm2.bestSol)
print(swarm3.bestSolValue, swarm3.bestSol)

gens = [i for i in range(1, swarm1.iter+1)]

fig, (a1, a2) = plt.subplots(2)
a1.plot(gens, swarm1.bestPerGen, 'r-', gens, swarm2.bestPerGen, 'g-', gens, swarm3.bestPerGen, 'b-')
a2.plot(gens, swarm1.averagePerGen, 'r-', gens, swarm2.averagePerGen, 'g-', gens, swarm3.averagePerGen, 'b-')

#plt.plot(gens, swarm1.bestPerGen, 'r-', gens, swarm2.bestPerGen, 'g-', gens, swarm3.bestPerGen, 'b-')
#a1.ylabel("Fitness of best particle in generation")
#a2.ylabel("Average fitness of population")
plt.xlabel("Generation #")
#plt.title("Best solution per generation vs. Generation #")
plt.show()

