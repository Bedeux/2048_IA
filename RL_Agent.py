import random
from Board import Board
from Game import Game
import time

class RLAgent:
    def __init__(self, board, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.2):
        self.board = board
        self.q_table = {}  # Utilisez une table Q pour stocker les valeurs Q
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.grid = None
        self.previous_grid = None
        self.availabe_moves = []
        self.empty_cells = -1
        self.max_value_cell = 0
        self.score = 0
        self.update_board_values(board)

    def choose_action(self, board):
        self.update_board_values(board)
        # Convertissez self.grid en un tuple de tuples
        state_tuple = tuple(tuple(row) for row in self.grid)

        # Choisissez une action en fonction de l'état et de la stratégie d'exploration
        if random.uniform(0, 1) < self.exploration_prob:
            if len(self.availabe_moves)>0:
                return random.choice(self.availabe_moves)
            else :
                return 'Down' # test to avoid error
        else:
            # Choisissez l'action avec la plus grande valeur Q
            max_q_value = float('-inf')
            best_action = None
            for action in self.availabe_moves:
                q_value = self.q_table.get((state_tuple, action), 0)
                if q_value > max_q_value:
                    max_q_value = q_value
                    best_action = action
            return best_action

    def update(self, state, action, reward, next_state):
        # Convertissez les listes 'state' et 'next_state' en tuples pour les utiliser comme clés
        state_tuple = tuple(tuple(row) for row in state)
        next_state_tuple = tuple(tuple(row) for row in next_state)

        # Mettez à jour la table Q en utilisant l'algorithme Q-learning
        current_q_value = self.q_table.get((state_tuple, action), 0)
        
        max_next_q_value = -1  # Définir une valeur par défaut basse
        if self.availabe_moves:
            max_next_q_value = max(self.q_table.get((next_state_tuple, a), -1) for a in self.availabe_moves)

        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)
        self.q_table[(state_tuple, action)] = new_q_value


    def update_board_values(self, board):
        self.board = board
        self.grid = board.get_cell_grid()
        self.previous_grid = board.get_previous_grid()
        self.availabe_moves = board.get_possible_moves()
        self.empty_cells = board.get_nb_empty_cells()
        self.max_value_cell = board.get_max_cell_value()
        self.score = board.get_score()

    def train(self, num_episodes):
        for episode in range(num_episodes):
            gamepanel = Board()
            game2048 = Game(gamepanel=gamepanel)
            game2048.start()

            initial_state = gamepanel.get_cell_grid()
            total_reward = 0

            iteration = 0
            while not game2048.end and not game2048.won:
                iteration = iteration+1

                action = self.choose_action(gamepanel)
                
                initial_score = gamepanel.get_score()
                initial_state = gamepanel.get_cell_grid()
                
                game2048.gamepanel.move(action)
                
                reward = gamepanel.get_score() - initial_score
                game2048.continue_game()

                next_state = gamepanel.get_cell_grid()
                self.update(initial_state, action, reward, next_state)

                total_reward += reward

            print(f"Épisode {episode + 1}: Récompense totale = {total_reward}")

