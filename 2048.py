import time
from Board import Board
from Game import Game

# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    start_time = time.time()
    n=0
    games_number = 1
    while n<games_number:
        n+=1
        gamepanel = Board()
        game2048 = Game(gamepanel)
        game2048.start()
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))


if __name__ == "__main__":
    main()