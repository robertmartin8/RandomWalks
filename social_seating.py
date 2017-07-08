import random
import statistics
import matplotlib.pyplot as plt


network = [[0, 2, 0, 0, 0, 0, 0, 0],
           [2, 0, 1, 0, 0, 0, 0, 1],
           [0, 1, 0, 1, 0, 0, 0, 0.5],
           [0, 0, 1, 0, 0.5, 2, 0, 0],
           [0, 0, 0, 0.5, 0, 1, 0, 0],
           [0, 0, 0, 2, 1, 0, 0.5, 0],
           [0, 0, 0, 0, 0, 0.5, 0, 2],
           [0, 1, 0.5, 0, 0, 0, 1, 0]]

network_size = len(network)
population_size = 16


def generate_population(network_size, population_size):
    """
    :param network_size: the number of individuals in the network
    :param population_size: the number of different initial arrangements
    """
    # Empty list which will contain the arrangements
    population = []
    # Produce the simplest arrangement, which is just the
    # individuals in order of their index, i.e [1,2,3,4,5,6,7,8].
    test_phenotype = [i for i in range(1, network_size + 1)]

    # Shuffle the test_phenotype to generate the population
    for i in range(population_size):
        random.shuffle(test_phenotype)
        population.append(list(test_phenotype))

    return population


def evaluate_etotal(arrangement):
    etotal = 0

    for r in range(network_size - 1):
        # u_r1 is meant to represent u_{r+1}
        # When defining u_r and u_r1, we subtract 1,
        # because indices in python start from zero.
        u_r = arrangement[r] - 1
        u_r1 = arrangement[r + 1] - 1

        # network[u_r][u_r1] is the same as [u_r, u_r1]
        # epair is the contribution from each pair
        epair = network[u_r][u_r1] + network[u_r1][u_r]
        etotal += epair

    return(etotal)


def survive_and_reproduce(population):
    # We will make a new list that stores the 'fitness' of each phenotype
    # in the population, where 'fitness' depends on the e_total.
    population_fitness = [evaluate_etotal(phenotype) for phenotype in population]

    # If a phenotype has an etotal lower than the median etotal, it is WEAK.
    median = statistics.median(population_fitness)
    weaklings = [i for i in range(len(population)) if population_fitness[i] < median]

    # Destroy the weak arrangements by excluding them from the survivor list
    survivors = [population[i] for i in range(len(population)) if i not in weaklings]

    number_removed = len(population) - len(survivors)

    # Now, the survivors 'breed'. This for loop maintains the population_size.
    for i in range(number_removed):
        # Pick a parent from the survivors
        parent = random.choice(survivors)
        # A child is the first half of a parent, plus the shuffled second half.
        estranged_father = parent[
                    int(network_size / 2):network_size]
        random.shuffle(estranged_father)
        child = parent[0:int(network_size / 2)] + estranged_father

        # The child is now part of the new generation
        survivors.append(child)

    return survivors


def mutate(generation, mutation_rate=0.05):
    # Each member of the population has a chance of being mutated
    for i in range(len(generation)):
        # random.random() returns a float between 0 and 1,
        # so this is equivalent to a probability of the mutation_rate.
        if random.random() < mutation_rate:
            # A mutation entails two elements of the arrangement swapping.
            a, b = random.sample(range(network_size), 2)
            population[i][b], population[i][a] = population[i][a], population[i][b]


progress_list = []
hall_of_fame = []


def progress(generation):
    population_fitness = [evaluate_etotal(phenotype) for phenotype in population]
    progress_list.append(max(population_fitness))
    max_location = population_fitness.index(max(population_fitness))
    hall_of_fame.append(population[max_location])


population = generate_population(network_size, 16)
gen_number = 500

while gen_number:
    next_generation = survive_and_reproduce(population)
    progress(next_generation)
    mutate(next_generation)
    population = next_generation

    if gen_number == 1:
        champion_location = progress_list.index(
                    max(progress_list))
        print("The optimal arrangement is: ", hall_of_fame[champion_location], ", with an etotal of: ",
              max(progress_list))

    gen_number -= 1

plt.plot(progress_list)
plt.title('Evolution of etotal')    
plt.xlabel('Generation number')
plt.ylabel(r'$\epsilon$ total')
plt.show()

