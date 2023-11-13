import time
from Board import Board
from Game import Game
from AI_DepthOne import AI_DepthOne
import argparse

def main(option):
    start_time = time.time()
    weights =   {'border': 0.96, 'biggest_adjacents': 0.806, 'future_merges': 0.388, 'empty_cells': 0.445, 'full_line': 0.509, 'weighted_sum': 0.139}
    ai_depth_one = AI_DepthOne(weights=weights)

    n=0
    games_number = 5
    scores = []
    while n<games_number:
        n+=1
        gamepanel = Board()
        game2048 = Game(gamepanel, option)
        game2048.start()
        while not game2048.end and not game2048.won:
            action = ai_depth_one.choose_action(gamepanel)
            game2048.gamepanel.move(action)
            game2048.continue_game(dipslay_moves=True) # Change display_move for quick games 
        scores.append(gamepanel.get_score())
    print("--- %s seconds ---" % (round(time.time() - start_time,1)))
    print("Max Score : ",max(scores))
    print("Average Score : ",round(sum(scores) / len(scores)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the game with options')
    parser.add_argument('option', nargs='?', default='None', help='Choose an option if you want (Display, Score, Screenshot)')
    # command example : python3 2048.py Display
    args = parser.parse_args()
    main(args.option)