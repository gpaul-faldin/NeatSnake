import neat
import threading
import statistics
import pickle
import random
import os
from time import sleep, time
from queue import Queue

import neat.genome
from game import snakeGame
from gui import PopulationGUI
from snakegui import SnakeGameGUI
import sys

storagePath = os.getcwd() + '/logs/'

class neatRun:

  def __init__(self, load=False, log=False):
    self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, os.getcwd() +'/neat-config.txt')
    if load:
      pop, species, generations = None, None, 0
      with open(storagePath + 'pop.pkl', 'rb') as f:
        pop = pickle.load(f)
      with open(storagePath + 'species.pkl', 'rb') as f:
        species = pickle.load(f)
      initial_state = pop, species, generations
      self.population = neat.Population(self.config, initial_state=initial_state)
    else:
      self.population = neat.Population(self.config)
    self.population.add_reporter(neat.StdOutReporter(True))
    self.population.add_reporter(neat.StatisticsReporter())
    self.generation = 0
    self.mapSize = 8
    self.population_lock = threading.Lock()
    self.population_size = 0
    self.previousBestGenome = None
    if log == True:
      self.snakeGui = SnakeGameGUI()
    # self.infoGui = PopulationGUI()

  def log_genome(self, genomes):
    fitnesses = [genome.fitness for _, genome in genomes if genome.fitness is not None]
    avg_fitness = sum(fitnesses) / len(fitnesses)
    rounded_avg_fitness = round(avg_fitness, 6)

    std_dev = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0

    best_genome = max(genomes, key=lambda g: g[1].fitness)
    self.previousBestGenome = best_genome[0]
    best_genome_object = best_genome[1]

    rounded_std_dev = round(std_dev, 6) 

    if self.generation != 0 and self.generation % 10 == 0:
      pop, species = self.population.population, self.population.species
      filenamePop = f"{storagePath}/pop.pkl"
      filenameSpecies = f"{storagePath}/species.pkl"
      with open(filenamePop, "wb") as f:
          pickle.dump(pop, f)
      with open(filenameSpecies, "wb") as f:
          pickle.dump(species, f)

    log_info = f"Generation: {self.generation}, Best Fitness: {best_genome_object.fitness}, Average Fitness: {rounded_avg_fitness}, Standard Deviation: {rounded_std_dev}\n"
    log_filename = f"{storagePath}/log.txt"

    with open(log_filename, "a+") as log_file:
        log_file.write(log_info)

  def __calculate_fitness(self):
    pass

  def __eval_genome(self, genome: neat.DefaultGenome, log: bool = False):
    net = neat.nn.FeedForwardNetwork.create(genome, self.config)
    game = snakeGame(self.mapSize, False)
    fitness = 0
    while not game.stop:
        inputs = game.snakeVision
        outputs = net.activate(inputs)
        direction = np.argmax(outputs)
        game.moveByMoveSimulation(direction)
        fitness += game.score
    return fitness

  def runTraining(self):
    self.population.run(self.runFunction)

  def runFunction(self, genomes: list[int, neat.DefaultGenome], config):
    fitness_values = []
    gameInstances = []

    for genome_id, genome in genomes:
      gameInstances.append(snakeGame(self.mapSize, False))

    for genome_id, genome in genomes:
      pass

    self.log_genome(fitness_values)
    self.generation += 1

def main(args):
  if len(args) > 0:
    neatInstance = neatRun(True)
  else:
    neatInstance = neatRun(False)
  neatInstance.runTraining()

if __name__ == "__main__":
  main(sys.argv[1:])
