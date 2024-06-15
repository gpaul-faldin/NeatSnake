import neat
import threading
import statistics
import pickle
import random
import os
from time import sleep, time
from queue import Queue

from copy import deepcopy
import neat.genome
from game import snakeGame
from gui import PopulationGUI
from snakegui import SnakeGameGUI
import sys

storagePath = os.getcwd() + '/logs/'

class neatRun:

  def __init__(self, load=False, log=True):
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
    self.mapSize = 5
    self.population_lock = threading.Lock()
    self.population_size = 0
    self.previousBestGenome = None
    if log == True:
      pass
      # self.snakeGui = SnakeGameGUI()
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

  def __calculate_fitness(self, score, lifetime, distanceTravelled, starved, status, distanceBetweenSnakeAndFood):
    # Normalize score between 0 and 1
    score_normalized = score / ((self.mapSize * 2) - 2)

    # Normalize lifetime to encourage longer survival
    lifetime_normalized = min(1, lifetime / (self.mapSize * 2))

    # Normalize distance to food to encourage proximity to food
    proximity_normalized = min(1, 1 / (distanceBetweenSnakeAndFood + 1))

    # Normalize distance traveled to encourage efficient movement
    if distanceTravelled == 0:
        distance_normalized = 0
    else:
        distance_normalized = min(1, (self.mapSize * 2 - 2) / distanceTravelled)

    # Include a penalty for starvation
    if starved:
        starvation_penalty = 0.1  # Adjust penalty strength as needed
    else:
        starvation_penalty = 0

    # Combine normalized factors with weighted coefficients
    # Adjust coefficients based on their importance relative to score
    fitness = (0.7 * score_normalized) + (0.2 * lifetime_normalized) + (0.1 * proximity_normalized) - starvation_penalty

    # Ensure fitness does not exceed 1
    fitness = min(1, fitness)

    return fitness

  def __eval_genome(self, genome: neat.DefaultGenome, log, simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision):
    net = neat.nn.FeedForwardNetwork.create(genome, self.config)
    game = snakeGame(self.mapSize, log)
    game.setGameSet(simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision)

    commandQueue = Queue(maxsize=1)
    dataQueue = Queue(maxsize=1)
    resultQueue = Queue(maxsize=1)

    gameThread = threading.Thread(target=game.mainLoop, args=(commandQueue, dataQueue, resultQueue))
    gameThread.start()

    startOfLife = time()
    lastFoodTime = time()
    distanceTravelled = 0
    previousScore = 0
    starved = False
    distanceBetweenSnakeAndFood = 0
    while gameThread.is_alive():
        if not dataQueue.empty():
          try:
            sb, snakeHeadDir, scoreData, foodP, vision, map = dataQueue.get(timeout=1)
            distanceBetweenSnakeAndFood = abs(sb[0][0] - foodP[0]) + abs(sb[0][1] - foodP[1])
            inputs = [scoreData, snakeHeadDir, vision[0], vision[1], vision[2], vision[3]]

            # if log:
            #   self.snakeGui.update_screen(sb, snakeHeadDir, scoreData, foodPosition, vision, map)
            output = net.activate(inputs)

            # if log:
            #   print(f'output: {output}')


            if output[0] >= 0 and output[0] < 0.2:
              commandQueue.put_nowait(0)  # Move up
            elif output[0] >= 0.2 and output[0] < 0.4:
              commandQueue.put_nowait(1)  # Move down
            elif output[0] >= 0.4 and output[0] < 0.6:
              commandQueue.put_nowait(2)  # Move left
            elif output[0] >= 0.6 and output[0] < 0.8:
              commandQueue.put_nowait(3)  # Move right
            elif output[0] >= 0.8 and output[0] <= 1:
              commandQueue.put_nowait(4)  # Do nothing (or any other action)

            # if output[0] > 0.5:
            #   commandQueue.put_nowait(0)  # Move up
            # elif output[1] > 0.5:
            #   commandQueue.put_nowait(1)  # Move down
            # elif output[2] > 0.5:
            #   commandQueue.put_nowait(2)  # Move left
            # elif output[3] > 0.5:
            #   commandQueue.put_nowait(3)  # Move right
            # elif output[4] > 0.5:
            #   commandQueue.put_nowait(4)  # Do nothing (or any other action)

            # Update the last food time if the snake eats
            if scoreData > previousScore:
                lastFoodTime = time()
                previousScore = scoreData

            distanceTravelled += 1
          except:
            continue
        else:
            if (log == False and time() - lastFoodTime > 5) or (log == True and time() - lastFoodTime > 20):
              print('starved')
              commandQueue.put('kill')
              starved = True
              break

        if log:
          sleep(0.5)
        else:
          sleep(0.00001)

    lifetime = time() - startOfLife
    
    # print(f'Stop: {game.stop} reason: {game.stopReason} resultQueue: {resultQueue.empty()}')

    while resultQueue.empty():
        print('waiting for result')
        sleep(0.05)
    status, scoreResult = resultQueue.get()
    if log:
      print(f'distanceTravelled: {distanceTravelled}, lifetime: {lifetime}, starved: {starved}')
      # self.snakeGui.reset_screen(scoreResult, starved, lifetime)
    if status == 'win':
        genome.fitness = 1
    else:
        genome.fitness = self.__calculate_fitness(scoreResult, lifetime, distanceTravelled, starved, status, distanceBetweenSnakeAndFood)

  def runTraining(self):
    self.population.run(self.runFunction)

  def get_population_size(self):
    with self.population_lock:
      return self.population_size

  def runFunction(self, genomes: list[int, neat.DefaultGenome], config):
    threads: list[threading.Thread] = []
    SimulationGame = snakeGame(self.mapSize)
    simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision = SimulationGame.getSimulationData()
    # SimulationGame.printMap()



    # print(f'simuMap: {simuMap}, snakeBody: {snakeBody}, snakeHeadDirection: {snakeHeadDirection}, foodPosition: {foodPosition}, snakeVision: {snakeVision}')
    # print("""
    #       =================================================================
    #       """)

    monitor = False


    for genome_id, genome in genomes:

      if monitor == False and self.previousBestGenome == None:
        # self.snakeGui.display_top_section(f"Generation: {self.generation}, Genome: {genome_id}")
        thread = threading.Thread(target=self.__eval_genome, args=(genome,True, deepcopy(simuMap), deepcopy(snakeBody), deepcopy(snakeHeadDirection), deepcopy(foodPosition), deepcopy(snakeVision)))
        monitor = True
      elif monitor == False and self.previousBestGenome != None and genome_id == self.previousBestGenome:
        # self.snakeGui.display_top_section(f"Generation: {self.generation}, Genome: {genome_id}")
        thread = threading.Thread(target=self.__eval_genome, args=(genome,True, deepcopy(simuMap), deepcopy(snakeBody), deepcopy(snakeHeadDirection), deepcopy(foodPosition), deepcopy(snakeVision)))
        monitor = True
      else:
        thread = threading.Thread(target=self.__eval_genome, args=(genome,False, deepcopy(simuMap), deepcopy(snakeBody), deepcopy(snakeHeadDirection), deepcopy(foodPosition), deepcopy(snakeVision)))
      threads.append(thread)

    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()

    self.log_genome(genomes)
    self.generation += 1


def main(args):
  if len(args) > 0:
    neatInstance = neatRun(True)
  else:
    neatInstance = neatRun(False)
  neatInstance.runTraining()

if __name__ == "__main__":
  main(sys.argv[1:])
