#Libraries to use
from random import choice, random, randint, sample, seed, shuffle
import numpy as np
from copy import deepcopy

"""
Evolutionary Algorithm
"""
def population(pop_size, grid):
	populations = []
	copy = grid
	for i in range(pop_size):
		population = grid
		for j in range(len(copy)):
			shuffle_sub_grid = [n for n in range(1, len(copy) + 1)]
			shuffle(shuffle_sub_grid)

			for k in range(len(copy)):
				if copy[j][k] is not None:
					population[j][k] = copy[j][k]

			for k in range(len(copy)):
				if population[j][k] is None:
					population[j][k] = shuffle_sub_grid.pop()

		populations.append(population)
	return populations

#This evaluates the pop
def evaluate_pop(pop):
	#Size of sudoku
	n = 9
	#Values needed to evaluate the row, column and sub grid
	values = np.zeros((n, n), dtype=int)
	row_count = np.zeros(n)
	column_count = np.zeros(n)
	column = 0
	row = 0
	sub_grid_count = np.zeros(n)
	sub_grid = 0

	#These are for the rows and each number within the rows
	for i in range(0, n):
		for j in range(0, n):
			row_count[values[i][j]-1] += 1

		row += (1.0/len(set(row_count)))/n
		row_count = np.zeros(n)

	#These are for the columns and each number within the columns
	for i in range(0, n):
		for j in range(0, n):
			column_count[values[i][j]-1] += 1

		column += (1.0/len(set(column_count)))/n
		column_count = np.zeros(n)

	for i in range(0, n, 3):
		for j in range(0, n, 3):
			#This is each sub grid so it goes down the rows
			sub_grid_count[values[i][j]-1] += 1
			sub_grid_count[values[i][j+1]-1] += 1
			sub_grid_count[values[i][j+2]-1] += 1

			#Row two
			sub_grid_count[values[i+1][j]-1] += 1
			sub_grid_count[values[i+1][j+1]-1] += 1
			sub_grid_count[values[i+1][j+2]-1] += 1

			#Row Three
			sub_grid_count[values[i+2][j]-1] += 1
			sub_grid_count[values[i+2][j+1]-1] += 1
			sub_grid_count[values[i+2][j+2]-1] += 1

			sub_grid += (1.0/len(set(sub_grid_count)))/n
			sub_grid_count = np.zeros(n)

	#Fitness calculation
	if(int(column)==1 and int(row)==1 and int(sub_grid)==1):
		fitness = 1.0
	else:
		fitness = row*column
	return fitness

#Selects the populations
def select_pop(population, fitness_population):
	old_pop = population
	new_pop = fitness_population
	sort = sorted(zip(old_pop, new_pop), key = lambda ind_fit: ind_fit[1])
	return [ individual for individual, fitness in sort[:int(population_size * truncation)] ]

#Crossover
def crossover_pop(mating_pool):
	point = random.randrange(1, mating_pool)

	childs = []
	#Uses childs as a way to do this
	childs.append(crossover_ind(choice(mating_pool), choice(mating_pool)))
	childs.append(crossover_ind(choice(mating_pool), choice(mating_pool)))

	#This should get two points of the mating pool and cross them over
	childs[0] = [:point] + [point:]
	childs[1] = [:point] + [point:]
	return childs

def crossover_ind(individual1, individual2):
	return [ choice(pair) for pair in zip(individual1, individual2) ]

#This should mutate the population by using a choice out of the numbers down below this
def mutate_pop(offspring_population):
	return [ mutate_ind(individual) for individual in offspring_population ]

def mutate_ind(individual):
	return [ (choice("123456789") if random() < mutation else nu) for nu in individual ]

"""
Generation of Sudoku
"""
#Loads the sudoku puzzle
def load():
	n = 9
	#Input unsolved sudoku like the file below to do a sudoku
	with open("sudoku_unsolved.txt", "r") as f:
		values = np.loadtxt(f).reshape((n, n)).astype(int)	
	return values

#Opens solved puzzle
def target():
	n = 9
	#Input solved sudoku like the file below to do a sudoku
	with open("sudoku_solved.txt", "r") as f:
		values = np.loadtxt(f).reshape((n, n)).astype(int)
	return values

"""
Main Execution
"""
def solve(pop_size, noofgen):
	target = target()
	individual_size = len(target)
	mutation = 0.05
	Truncation = 0.5
	grid = load()
	pop = population(pop_size, grid)
	fitness_population = evaluate_pop(pop)
	for generation in range(noofgen):
		g = str(generation)
		
		print("This is Generation " + g)
		fitness = evaluate_pop(pop)
		
		if(fitness == 1):
			print("Solution is found")
			return pop
		if(fitness > best_fitness):
			best_fitness = fitness

		fit = str(best_fitness)
		print("fitness: " + best_fitness)

		mating_pool = select_pop(pop, fitness_population)
		offspring_population = crossover_pop(mating_pool)
		pop = mutate_pop(offspring_population)
		fitness_population = evaluate_pop(pop)
        
"""
Values & Where Program Starts
"""
n = 9 #This is the 9 by 9 grid
population_size = 1000
noofgen = 1000
solve(population_size, noofgen)