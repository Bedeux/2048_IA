import time
from Board import Board
from Game import Game
from AI_DepthOne import AI_DepthOne

# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

def main():
    best_average_score = 0
    best_weights = None
    weights_combination = get_all_weights(step=0.2)
    print(len(weights_combination))
    for weights in weights_combination:
        print(weights)
        start_time = time.time()
        gamepanel = Board()
        gamepanel.window.after(0, lambda: gamepanel.window.destroy())
        ai_depth_one = AI_DepthOne(gamepanel,weights) 
        n=0
        games_number = 10
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
            
            if n==3 and round(sum(scores) / len(scores))<5000:
                n = games_number # end the loop
                print('END : bad parameters')
                
        average_score = round(sum(scores) / len(scores))
        print("--- %s seconds ---" % (round(time.time() - start_time,1)))
        print("Max Score : ",max(scores))
        print("Average Score : ",average_score)

        if average_score > best_average_score:
            best_average_score = average_score
            best_weights = weights
            print("Best average score : ",best_average_score," | Weights : ",best_weights)
    print("Best average score : ",best_average_score," | Weights : ",best_weights)

def round_to_nearest_0_2(number):
    return round(number * 5) / 5

def normalize_weights(weights):
    max_weight = max(weights.values())
    if max_weight == 0 or max_weight == 1:
        return weights  

    normalization_factor = 1 / max_weight
    normalized_weights = {k: round_to_nearest_0_2(v * normalization_factor) for k, v in weights.items()}
    return normalized_weights

def get_all_weights(step):
    num_steps = int(1 / step) + 1
    weights_combination = []
    for border_weight in [round(x * step, 1) for x in range(num_steps)]:
        for adjacents_weight in [round(x * step, 1) for x in range(num_steps)]:
            for future_merges_weight in [round(x * step, 1) for x in range(num_steps)]:
                for empty_cells_weight in [round(x * step, 1) for x in range(num_steps)]:
                    weight_combination = {
                        'border': border_weight,
                        'biggest_adjacents': adjacents_weight,
                        'future_merges': future_merges_weight,
                        'empty_cells': empty_cells_weight
                    }
                    combination_normalized = normalize_weights(weight_combination)
                    if combination_normalized not in weights_combination:
                        weights_combination.append(combination_normalized)
    return weights_combination


if __name__ == "__main__":
    main()