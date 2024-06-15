import random
from time import sleep
from queue import Queue
from snakegui import SnakeGameGUI

class snakeGame:

  def __init__(self, mapSize: int = 8, log:bool = False) -> None:
    self.mapsize = mapSize
    self.score = 0
    self.map = None
    self.snakeBody = []
    self.snakeHeadDirection = 0
    self.snakeVision = [0, 0, 0, 0, 0, 0, 0, 0]
    self.possiblePosition = [0, 1, 2, 3]
    self.foodPosition = [0, 0]
    self.directionList = ['up', 'down', 'left', 'right', 'nothing']
    self.stop = False
    self.stopReason = None
    self.__initMap()
    self.log = log

  def printMap(self, debug = False):
    for i in range(self.mapsize):
      print(self.map[i])
    print('---------------------------')
    if debug:
      return [self.map, self.snakeBody, self.foodPosition]
    return None
  
  def __generateMap(self):
    map = [[0 for i in range(self.mapsize)] for j in range(self.mapsize)]
    return map
  
  def __checkInitialDirection(self):
    if self.snakeHeadDirection == 0 and self.snakeBody[0][0] == 0:
      return False
    elif self.snakeHeadDirection == 1 and self.snakeBody[0][0] == self.mapsize-1:
      return False
    elif self.snakeHeadDirection == 2 and self.snakeBody[0][1] == 0:
      return False
    elif self.snakeHeadDirection == 3 and self.snakeBody[0][1] == self.mapsize-1:
      return False
    return True

  def __generateInitialBody(self, size:int = 1):
    if self.snakeHeadDirection == 0:
      for i in range(1, size+1):
        newBodyPosition = [self.snakeBody[0][0]+i, self.snakeBody[0][1]]
        if newBodyPosition == self.foodPosition:
          self.__generateFood()
        self.snakeBody.append(newBodyPosition)
    elif self.snakeHeadDirection == 1:
      for i in range(1, size+1):
        newBodyPosition = [self.snakeBody[0][0]-i, self.snakeBody[0][1]]
        if newBodyPosition == self.foodPosition:
          self.__generateFood()
        self.snakeBody.append(newBodyPosition)
    elif self.snakeHeadDirection == 2:
      for i in range(1, size+1):
        newBodyPosition = [self.snakeBody[0][0], self.snakeBody[0][1]+i]
        if newBodyPosition == self.foodPosition:
          self.__generateFood()
        self.snakeBody.append(newBodyPosition)
    elif self.snakeHeadDirection == 3:
      for i in range(1, size+1):
        newBodyPosition = [self.snakeBody[0][0], self.snakeBody[0][1]-i]
        if newBodyPosition == self.foodPosition:
          self.__generateFood()
        self.snakeBody.append(newBodyPosition)

  def __initMap(self):
    self.map = self.__generateMap()
    snakeHeadPosition = [random.randint(0, self.mapsize-1), random.randint(0, self.mapsize-1)]
    while snakeHeadPosition[0] == 0 or snakeHeadPosition[1] == 0 or snakeHeadPosition[0] == self.mapsize-1 or snakeHeadPosition[1] == self.mapsize-1:
        snakeHeadPosition = [random.randint(0, self.mapsize-1), random.randint(0, self.mapsize-1)]
    self.snakeBody.append(snakeHeadPosition)
    self.snakeHeadDirection = random.choice(self.possiblePosition)
    while self.__checkInitialDirection() == False:
        self.snakeHeadDirection = random.choice(self.possiblePosition)
    self.__generateInitialBody()
    self.__generateFood()

    self.map[self.snakeBody[0][0]][self.snakeBody[0][1]] = 1
    self.map[self.snakeBody[1][0]][self.snakeBody[1][1]] = 2
    self.map[self.foodPosition[0]][self.foodPosition[1]] = 3
    self.__snakeVision()

  def __checkWinner(self):
    if len(self.snakeBody) == self.mapsize * self.mapsize - 2: # -2 because head + body already occupied 2 cells
      self.stop = True
      self.stopReason = 'win'

  def __generateFood(self):
    self.map[self.foodPosition[0]][self.foodPosition[1]] = 0
    possible_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    if self.score < 2:
          # right, left, down, up
        random_direction = random.choice(possible_directions)
        new_food_position = [self.snakeBody[0][0] + random_direction[0], self.snakeBody[0][1] + random_direction[1]]
        while not (0 <= new_food_position[0] < self.mapsize and 0 <= new_food_position[1] < self.mapsize and
                   new_food_position not in self.snakeBody):
            random_direction = random.choice(possible_directions)
            new_food_position = [self.snakeBody[0][0] + random_direction[0], self.snakeBody[0][1] + random_direction[1]]
        self.foodPosition = new_food_position
    elif self.score < 4:
      possible_directions = [[2, 0], [-2, 0], [0, 2], [0, -2]]
      random_direction = random.choice(possible_directions)
      new_food_position = [self.snakeBody[0][0] + random_direction[0], self.snakeBody[0][1] + random_direction[1]]
      while not (0 <= new_food_position[0] < self.mapsize and 0 <= new_food_position[1] < self.mapsize and
                 new_food_position not in self.snakeBody):
          random_direction = random.choice(possible_directions)
          new_food_position = [self.snakeBody[0][0] + random_direction[0], self.snakeBody[0][1] + random_direction[1]]
      self.foodPosition = new_food_position
    else:
      self.map[self.foodPosition[0]][self.foodPosition[1]] = 0
      self.foodPosition = [random.randint(0, self.mapsize-1), random.randint(0, self.mapsize-1)]
      while self.foodPosition == self.snakeBody[0] or self.foodPosition in self.snakeBody:
          self.foodPosition = [random.randint(0, self.mapsize-1), random.randint(0, self.mapsize-1)]
    self.map[self.foodPosition[0]][self.foodPosition[1]] = 3

  def __clearBody(self):
    for i in range(len(self.snakeBody)):
      self.map[self.snakeBody[i][0]][self.snakeBody[i][1]] = 0

  def __addBodyToMap(self):
    for i in range(1, len(self.snakeBody)):
      self.map[self.snakeBody[i][0]][self.snakeBody[i][1]] = 2
    self.map[self.snakeBody[0][0]][self.snakeBody[0][1]] = 1

  def __checkCollision(self, nextPosition, safe = False):
    if nextPosition in self.snakeBody:
      if safe == False :
        self.stop = True
        self.stopReason = 'itself'
      return True
    elif nextPosition[0] < 0 or nextPosition[0] >= self.mapsize or nextPosition[1] < 0 or nextPosition[1] >= self.mapsize:
      if safe == False:
        self.stop = True
        self.stopReason = 'wall'
      return True
    return False

  def __addBody(self):
    self.__clearBody()
    newBodyPosition = None
    if self.snakeHeadDirection == 0:
      newBodyPosition = [self.snakeBody[self.score + 1][0]+1, self.snakeBody[self.score + 1][1]]
    elif self.snakeHeadDirection == 1:
      newBodyPosition = [self.snakeBody[self.score + 1][0]-1, self.snakeBody[self.score + 1][1]]
    elif self.snakeHeadDirection == 2:
      newBodyPosition = [self.snakeBody[self.score + 1][0], self.snakeBody[self.score + 1][1]+1]
    elif self.snakeHeadDirection == 3:
      newBodyPosition = [self.snakeBody[self.score + 1][0], self.snakeBody[self.score + 1][1]-1]

    if self.__checkCollision(newBodyPosition, True):
      directions = [0, 1, 2, 3]
      directions.remove(self.snakeHeadDirection)  # Remove the current direction
      while directions:
        direction = random.choice(directions)
        if direction == 0:
          newBodyPosition = [self.snakeBody[self.score + 1][0]+1, self.snakeBody[self.score + 1][1]]
        elif direction == 1:
          newBodyPosition = [self.snakeBody[self.score + 1][0]-1, self.snakeBody[self.score + 1][1]]
        elif direction == 2:
          newBodyPosition = [self.snakeBody[self.score + 1][0], self.snakeBody[self.score + 1][1]+1]
        elif direction == 3:
          newBodyPosition = [self.snakeBody[self.score + 1][0], self.snakeBody[self.score + 1][1]-1]
        if not self.__checkCollision(newBodyPosition, True):
          self.snakeHeadDirection = direction
          break
        directions.remove(direction)

    self.snakeBody.append(newBodyPosition)
    self.__addBodyToMap()
    self.score += 1
    return True

  def __eatingFood(self, nextPosition):
    if nextPosition == self.foodPosition:
      self.__addBody()
      self.__checkWinner()
      if self.stop == False:
        self.__generateFood()
      return True
    return False

  def __snakeVision(self):
    vision = [0, 0, 0, 0, 0, 0, 0, 0] # [up, down, left, right, up-left, up-right, down-left, down-right]

    #Check if the snake is at the edge of the map
    if self.snakeBody[0][0] - 1 == -1:
      vision[0] = 1
    if self.snakeBody[0][0] + 1 == self.mapsize:
      vision[1] = 1
    if self.snakeBody[0][1] - 1 == -1:
      vision[2] = 1
    if self.snakeBody[0][1] + 1 == self.mapsize:
      vision[3] = 1

    # Check diagonal map edges
    # if self.snakeBody[0][0] - 1 == -1 or self.snakeBody[0][1] - 1 == -1:
    #   vision[4] = 1
    # if self.snakeBody[0][0] - 1 == -1 or self.snakeBody[0][1] + 1 == self.mapsize:
    #   vision[5] = 1
    # if self.snakeBody[0][0] + 1 == self.mapsize or self.snakeBody[0][1] - 1 == -1:
    #   vision[6] = 1
    # if self.snakeBody[0][0] + 1 == self.mapsize or self.snakeBody[0][1] + 1 == self.mapsize:
    #   vision[7] = 1


    #Check if there is a body part in the next cell
    if vision[0] == 0 and self.map[self.snakeBody[0][0] - 1][self.snakeBody[0][1]] == 2:
      vision[0] = 2
    if vision[1] == 0 and self.map[self.snakeBody[0][0] + 1][self.snakeBody[0][1]] == 2:
      vision[1] = 2
    if vision[2] == 0 and self.map[self.snakeBody[0][0]][self.snakeBody[0][1]-1] == 2:
      vision[2] = 2
    if vision[3] == 0 and self.map[self.snakeBody[0][0]][self.snakeBody[0][1]+1] == 2:
      vision[3] = 2

    #check diagonal body parts
    # if vision[4] == 0 and self.map[self.snakeBody[0][0] - 1][self.snakeBody[0][1] - 1] == 2:
    #   vision[4] = 2
    # if vision[5] == 0 and self.map[self.snakeBody[0][0] - 1][self.snakeBody[0][1] + 1] == 2:
    #   vision[5] = 2
    # if vision[6] == 0 and self.map[self.snakeBody[0][0] + 1][self.snakeBody[0][1] - 1] == 2:
    #   vision[6] = 2
    # if vision[7] == 0 and self.map[self.snakeBody[0][0] + 1][self.snakeBody[0][1] + 1] == 2:
    #   vision[7] = 2

    #Check if there is a food in the next cell
    if vision[0] == 0 and self.map[self.snakeBody[0][0]-1][self.snakeBody[0][1]] == 3:
      vision[0] = 3
    if vision[1] == 0 and self.map[self.snakeBody[0][0]+1][self.snakeBody[0][1]] == 3:
      vision[1] = 3
    if vision[2] == 0 and self.map[self.snakeBody[0][0]][self.snakeBody[0][1]-1] == 3:
      vision[2] = 3
    if vision[3] == 0 and self.map[self.snakeBody[0][0]][self.snakeBody[0][1]+1] == 3:
      vision[3] = 3

    #check diagonal food
    # if vision[4] == 0 and self.map[self.snakeBody[0][0] - 1][self.snakeBody[0][1] - 1] == 3:
    #   vision[4] = 3
    # if vision[5] == 0 and self.map[self.snakeBody[0][0] - 1][self.snakeBody[0][1] + 1] == 3:
    #   vision[5] = 3
    # if vision[6] == 0 and self.map[self.snakeBody[0][0] + 1][self.snakeBody[0][1] - 1] == 3:
    #   vision[6] = 3
    # if vision[7] == 0 and self.map[self.snakeBody[0][0] + 1][self.snakeBody[0][1] + 1] == 3:
    #   vision[7] = 3

    self.snakeVision = vision

  def __getNextPosition(self, direction):
    
    if direction in self.possiblePosition:
      self.snakeHeadDirection = direction

    if self.snakeHeadDirection == 0:
      return [self.snakeBody[0][0]-1, self.snakeBody[0][1]]
    elif self.snakeHeadDirection == 1:
      return [self.snakeBody[0][0]+1, self.snakeBody[0][1]]
    elif self.snakeHeadDirection == 2:
      return [self.snakeBody[0][0], self.snakeBody[0][1]-1]
    elif self.snakeHeadDirection == 3:
      return [self.snakeBody[0][0], self.snakeBody[0][1]+1]

  def __move(self, direction):

    self.__clearBody()
    nextPosition = self.__getNextPosition(direction)

    if self.__checkCollision(nextPosition):
      return False

    self.snakeBody.pop()
    self.snakeBody.insert(0, nextPosition)

    self.__eatingFood(nextPosition)
    self.__addBodyToMap()

    self.__snakeVision()
    return True

  def getSimulationData(self):
    return [self.map, self.snakeBody, self.snakeHeadDirection ,self.foodPosition, self.snakeVision]

  def setGameSet(self, simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision):
    self.map = simuMap
    self.snakeBody = snakeBody
    self.snakeHeadDirection = snakeHeadDirection
    self.foodPosition = foodPosition
    self.snakeVision = snakeVision

  def mainLoop(self, commandQueue: Queue, dataQueue: Queue, resultQueue: Queue):

    sleep(0.01)
    # dataQueue.put([self.snakeBody, self.snakeHeadDirection, self.score, self.foodPosition, self.snakeVision, self.map])
    while True:

      direction = self.snakeHeadDirection

      if self.stop:
        resultQueue.put([self.stopReason, self.score])
        break


      if not commandQueue.empty():
        command = commandQueue.get_nowait()
        commandQueue.task_done()
        if command == "kill":
          resultQueue.put(['lose', self.score])
          break
        direction = command

      # if self.log:
      #   print(f'direction: {self.directionList[direction]}')
      #   print(f'score: {self.score}')
      #   print(f'snakeBody: {self.snakeBody}')
      #   print(f'snakeHeadDirection: {self.snakeHeadDirection}')
      #   print(f'snakeVision: {self.snakeVision}')
      #   print("Before Move")
      #   self.printMap()
      self.__move(direction)
      if self.log:
        # print("After Move")
        self.printMap()
      dataQueue.put([self.snakeBody, self.snakeHeadDirection ,self.score, self.foodPosition, self.snakeVision, self.map])
      if self.stop:
        resultQueue.put([self.stopReason, self.score])
        break

      if self.log:
        sleep(0.8)
      else:
        sleep(0.0001)
