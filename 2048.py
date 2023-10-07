import time
from Board import Board
from Game import Game
from RL_Agent import RLAgent
import json  # Pour lire la Q-table à partir d'un fichier JSON
import ast



# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    start_time = time.time()
    gamepanel = Board()
    gamepanel.window.after(1, lambda: gamepanel.window.destroy())
    rl_agent = RLAgent(gamepanel) 
    rl_agent.load_q_table('q_table.json')

    n=0
    games_number = 10
    while n<games_number:
        n+=1
        gamepanel = Board()
        game2048 = Game(gamepanel)
        game2048.start()
        while not game2048.end and not game2048.won:
            action = rl_agent.choose_action(gamepanel)
            game2048.gamepanel.move(action)
            game2048.continue_game()
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))
    # TODO Idée : multiplier par 2 les valeurs de la Q table (et même par 4) 
    # pour reproduire les mêmes scénarios avec les rewards associés 

    # TODO Idée : si scénario unique éxecuter le mouvement le plus reproduit durant la partie, 
    # et sinon le deuxieme, etc



def train_rl_model_q_table():
    num_episodes = 5000
    gamepanel = Board()
    gamepanel.window.after(1, lambda: gamepanel.window.destroy())
    rl_agent = RLAgent(gamepanel,exploration_prob=1) 
    rl_agent.train(num_episodes) 
    q_table_str_keys = {str(key): value for key, value in rl_agent.q_table.items()}
    with open('q_table.json', 'w') as json_file:
        json.dump(q_table_str_keys, json_file)

def several_actions_for_position():
    gamepanel = Board()
    gamepanel.window.after(1, lambda: gamepanel.window.destroy())
    rl_agent = RLAgent(gamepanel) 
    rl_agent.load_q_table('q_table.json')
    multiple_actions_count = 0
    one_action_count = 0
    state_action_counts = {}

    for state_action in rl_agent.q_table.items():
        value = state_action[0]
        
        action = value.split(", '")[1][:-2]
        state = value.split(", '")[0]
        if state in state_action_counts:
            state_action_counts[state].append(action)
        else:
            state_action_counts[state] = [action]

    for state, actions in state_action_counts.items():
        if len(actions) > 1:
            multiple_actions_count += 1
        else : 
            one_action_count +=1

    print("Nombre de positions avec plusieurs actions associées :", multiple_actions_count)
    print("Nombre de positions avec une seule action associée :", one_action_count)


if __name__ == "__main__":
    main()