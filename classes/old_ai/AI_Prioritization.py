import time
from classes.Board import Board
from classes.Game import Game
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
        # rl_agent.train(num_episodes) 
        game2048.start()
        possible_actions = ["Down", "Right", "Left", 'Up'] # in order of prioritization
        grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        last_action = "Up"
        while not game2048.end and not game2048.won:
            # If the grid changes (bug with the reversed grid), do the first move possible 
            if game2048.gamepanel.different_states(game2048.gamepanel.get_cell_grid(),grid) and game2048.gamepanel.different_states(game2048.gamepanel.get_cell_grid(),reverse_element_order(grid)):
                prioritization_action = "Down"
                last_action = "Down"
            # Else do the next action possible
            else : 
                action_index = possible_actions.index(last_action)
                prioritization_action = possible_actions[action_index + 1]
                last_action = possible_actions[action_index + 1]
            grid = game2048.gamepanel.get_cell_grid()
            game2048.gamepanel.move(prioritization_action)
            
            game2048.continue_game()
        scores.append(gamepanel.get_score())
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))
    print("Max Score : ",max(scores))
    print("Average Score : ",round(sum(scores) / len(scores)))


def reverse_element_order(lst):
    result = []
    for sub_list in lst:
        reversed_sub_list = sub_list[::-1]
        result.append(reversed_sub_list)
    return result


if __name__ == "__main__":
    main()