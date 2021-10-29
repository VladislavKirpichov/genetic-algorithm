import random
import matplotlib.pyplot as plt

# constants
LENGTH = 100                # line length
POPULATION_LENGTH = 100     # number of individuals in the population
P_CROSSOVER = 0.8           # crossover probability
P_MUTATION = 0.1            # mutation probability
MAX_GENERATIONS = 200       # maximum number of generations

maxFitnessValues = []       # maximum fitness in the population
meanFitnessValues = []      # average fitness in the population


class Fitness():
    def __init__(self) -> list:
        self.values = [0]


class Individual(list):
    def __init__(self, *args) -> list:
        super().__init__(*args)
        self.fitness = Fitness()


def makeFitness(individual):
    return sum(individual)


population = [Individual([random.randint(0, 1) for i in range(LENGTH)]) for i in
              range(POPULATION_LENGTH)]  # генерация популяции

fitnessValues = list(map(makeFitness, population))

for individual, value in zip(population, fitnessValues):  # consider fitness
    individual.fitness.values[0] = value


def clone(individual):
    ind = Individual(individual[:])
    ind.fitness.values[0] = makeFitness(individual)
    return ind


def tournament(population) -> list:
    result = []

    for i in range(len(population)):
        i1 = i2 = i3 = 0

        while i1 == i2 or i2 == i3 or i1 == i3:
            i1, i2, i3 = random.randint(0, len(population) - 1), random.randint(0, len(population) - 1), random.randint(
                0, len(population) - 1)

        result.append(max([population[i1], population[i2], population[i3]]))

    return result


def selection(parent1, parent2):
    divider = random.randint(1, 98)
    parent1[divider:], parent2[divider:] = parent2[divider:], parent1[divider:]


def mutation(mutant) -> list:
    randInt = random.randint(0, 99)
    if mutant[randInt] == 1:
        mutant[randInt] = 0
    else:
        mutant[randInt] = 1


counter = 0
while max(fitnessValues) != LENGTH and counter != MAX_GENERATIONS:

    newPopulation = tournament(population)
    newPopulation = list(map(clone, newPopulation))

    for parent1, parent2 in zip(newPopulation[::2], newPopulation[1::2]):
        if random.random() < P_CROSSOVER:
            selection(parent1, parent2)

    for mutant in newPopulation:
        if random.random() < P_MUTATION:
            mutation(mutant)

    fitnessValues = list(map(makeFitness, newPopulation))

    for individual, value in zip(newPopulation, fitnessValues):
        individual.fitness = value

    population[:] = newPopulation
    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(population)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)

    print(f'Поколение№{counter + 1}, Лучшая приспособленность = {maxFitness}, Средняя приспособленность = {meanFitness}')
    counter += 1

plt.plot(maxFitnessValues, color='blue')
plt.plot(meanFitnessValues, color='black')
plt.xlabel('Поколение')
plt.ylabel('Макс/сред приспособленность')
plt.show()
