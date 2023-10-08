import random
from Board import Board
from Game import Game
import time
import json

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

    def load_q_table(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.q_table = json.load(file)
        except FileNotFoundError:
            print(f"File {file_name} not found")

    def choose_action(self, board):
        self.update_board_values(board)
        # Convertissez self.grid en un tuple de tuples
        state_tuple = tuple(tuple(row) for row in self.grid)

        state_tuple = str(state_tuple) # JSON File get str of tuples

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
                
                # print(action,'  ',state_tuple,'  ',q_value)
                if q_value > max_q_value:
                    max_q_value = q_value
                    best_action = action
            return best_action

    def update(self, state, action, reward, next_state):
        # Convertissez les listes 'state' et 'next_state' en tuples pour les utiliser comme clés
        state_tuple = tuple(tuple(row) for row in state)
        next_state_tuple = tuple(tuple(row) for row in next_state)
        
        # Vérifiez si une entrée existe déjà pour cet état et cette action
        if (state_tuple, action) not in self.q_table:
            self.q_table[(state_tuple, action)] = 0.0
        
        # Mettez à jour la table Q en utilisant l'algorithme Q-learning
        current_q_value = self.q_table[(state_tuple, action)]

        max_next_q_value = -1  # Définir une valeur par défaut basse
        if self.availabe_moves:
            max_next_q_value = max(self.q_table.get((next_state_tuple, a), -1) for a in self.availabe_moves)

        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)
        self.q_table[(state_tuple, action)] = round(new_q_value, 3)


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
                initial_empty_cells = gamepanel.get_nb_empty_cells()
                initial_state = gamepanel.get_cell_grid()
                
                game2048.gamepanel.move(action)
                
                score_diff = gamepanel.get_score() - initial_score
                empty_cells_diff = gamepanel.get_nb_empty_cells() - initial_empty_cells
                reward = score_diff + empty_cells_diff
                
                game2048.continue_game()

                next_state = gamepanel.get_cell_grid()
                self.update(initial_state, action, reward, next_state)
                self.update_rotations(initial_state, action, reward, next_state)

                total_reward += reward

            print(f"Épisode {episode + 1}: Récompense totale = {total_reward}")

    def update_rotations(self,initial_state, action, reward, next_state):
        """Update the Q table with same positions of 2048 pivoted"""
        original_rotated_90 = tuple(zip(*initial_state[::-1]))
        new_rotated_90 = tuple(zip(*next_state[::-1]))
        action_90 = self.adapt_action(action,90)
        self.update(original_rotated_90, action_90, reward, new_rotated_90)

        original_rotated_180 = tuple(tuple(row[::-1]) for row in reversed(initial_state))
        new_rotated_180 = tuple(tuple(row[::-1]) for row in reversed(next_state))
        action_180 = self.adapt_action(action,180)
        self.update(original_rotated_180, action_180, reward, new_rotated_180)

        original_rotated_270 = tuple(tuple(initial_state[j][i] for j in range(len(initial_state))) for i in range(len(initial_state) - 1, -1, -1))
        new_rotated_270 = tuple(tuple(next_state[j][i] for j in range(len(next_state))) for i in range(len(next_state) - 1, -1, -1))
        action_270 = self.adapt_action(action,270)
        self.update(original_rotated_270, action_270, reward, new_rotated_270)
        
    def adapt_action(self,action, degrees):
        """From an action, create the same action with a pivot in degrees"""
        action_mapping = {
            "Up": "Right",
            "Down": "Left",
            "Left": "Up",
            "Right": "Down"
        }
        if degrees == 90:
            return action_mapping.get(action, action)
        elif degrees == 180:
            return action_mapping.get(action_mapping.get(action, action), action)
        elif degrees == 270:
            return action_mapping.get(action_mapping.get(action_mapping.get(action, action), action), action)
        else:
            return action  # Initial action