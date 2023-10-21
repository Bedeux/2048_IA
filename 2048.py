import time
from Board import Board
from Game import Game
from RL_Agent import RLAgent
from AI_DepthOne import AI_DepthOne

# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    start_time = time.time()
    gamepanel = Board()
    gamepanel.window.after(1, lambda: gamepanel.window.destroy())
    ai_depth_one = AI_DepthOne(gamepanel) 

    n=0
    games_number = 100
    scores = []
    while n<games_number:
        n+=1
        gamepanel = Board()
        game2048 = Game(gamepanel)
        game2048.start()
        while not game2048.end and not game2048.won:
            action = ai_depth_one.choose_action(gamepanel)
            game2048.gamepanel.move(action)
            game2048.continue_game()
        scores.append(gamepanel.get_score())
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))
    print("Max Score : ",max(scores))
    print("Average Score : ",round(sum(scores) / len(scores)))
    # TODO Idée : multiplier par 2 les valeurs de la Q table (et même par 4) 
    # pour reproduire les mêmes scénarios avec les rewards associés 

    # TODO Idée : si scénario unique éxecuter le mouvement le plus reproduit durant la partie, 
    # et sinon le deuxieme, etc

if __name__ == "__main__":
    main()