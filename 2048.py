import time
from Board import Board
from Game import Game
from RL_Agent import RLAgent

# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    start_time = time.time()
    n=0
    games_number = 1
    num_episodes = 10
    while n<games_number:
        n+=1
        gamepanel = Board()
        gamepanel.window.after(1, lambda: gamepanel.window.destroy())
        rl_agent = RLAgent(gamepanel) 
        rl_agent.train(num_episodes) 

        # game2048 = Game(gamepanel)
        # game2048.start()
    print(rl_agent.q_table)
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))


if __name__ == "__main__":
    main()