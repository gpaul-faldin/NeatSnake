from game import snakeGame
from queue import Queue
from threading import Thread
from time import sleep

def printMap(map):
  for i in range(8):
    print(map[i])
  print('---------------------------')

def main():
  
    simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision = snakeGame(8).getSimulationData()


    simuMap = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0]]
    snakeBody = [[5, 5], [5, 6]]
    snakeHeadDirection = 2
    foodPosition = [7, 5]
    snakeVision = [0, 0, 0, 2, 0, 0, 0, 0]

      # printMap(simuMap)
      
      # newSimu = snakeGame(8)
      # newSimu.setGameSet(simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision)
      # newSimu.printMap()
  
    game = snakeGame(8, True)
    print("Original Map")
    game.printMap()
    print('==================================================')
    game.setGameSet(simuMap, snakeBody, snakeHeadDirection, foodPosition, snakeVision)
    commandQueue = Queue()
    dataQueue = Queue()
    resultQueue = Queue()

    # game.printMap()
    gameThread = Thread(target=game.mainLoop, args=(commandQueue, dataQueue, resultQueue)) #game.mainLoop(commandQueue, dataQueue, resultQueue)
    gameThread.start()

    while True:

      # commandQueue.put(0)

      commandQueue.put(int(input()))

      if not resultQueue.empty():
        result = resultQueue.get_nowait()
        print(result)
        if result:
          break
      if not dataQueue.empty():
        data = dataQueue.get_nowait()
        # game.printMap()
    sleep(1)


main()