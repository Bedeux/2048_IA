import optuna # To install this package : pip install optuna
from Board import Board
from Game import Game
from AI_DepthOne import AI_DepthOne

def objective(trial):
    weights = {
        'border': trial.suggest_uniform('border', 0, 1),
        'biggest_adjacents': trial.suggest_uniform('biggest_adjacents', 0, 1),
        'future_merges': trial.suggest_uniform('future_merges', 0, 1),
        'empty_cells': trial.suggest_uniform('empty_cells', 0, 1),
        'full_line': trial.suggest_uniform('full_line', 0, 1),
        'weighted_sum': trial.suggest_uniform('weighted_sum', 0, 1)
    }

    games_number = 25
    scores = []
    for _ in range(games_number):
        gamepanel = Board()
        game2048 = Game(gamepanel, None)
        game2048.start()
        ai_depth_one = AI_DepthOne(weights)
        while not game2048.end and not game2048.won:
            action = ai_depth_one.choose_action(gamepanel)
            game2048.gamepanel.move(action)
            game2048.continue_game()
        scores.append(gamepanel.get_score())

    average_score = round(sum(scores) / len(scores))
    return -average_score

if __name__ == "__main__":
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=100)  
    
    best_params = study.best_params
    best_average_score = -study.best_value

    print("Best average score:", best_average_score)
    print("Best weights:", best_params)
