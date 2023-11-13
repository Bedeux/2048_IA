import time
from Board import Board
from Game import Game
import random


# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    start_time = time.time()
    n=0
    games_number = 100
    scores = []
    while n<games_number:
        n+=1
        gamepanel = Board()
        game2048 = Game(gamepanel, 'Display')
        game2048.start()
        possible_actions = ["Up", "Down", "Right", "Left"]
        while not game2048.end and not game2048.won:
            random_action = random.choice(possible_actions)
            game2048.gamepanel.move(random_action)
            game2048.continue_game()
        scores.append(gamepanel.get_score())
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))
    print("Max Score : ",max(scores))
    print("Average Score : ",round(sum(scores) / len(scores)))


if __name__ == "__main__":
    main()