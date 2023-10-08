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
            if len(self.availabe_moves)>0:
                best_action = random.choice(self.availabe_moves)
            else :
                best_action = 'Down'
            
            for action in self.availabe_moves:
                q_value = self.q_table.get((state_tuple, action), 0)
                if q_value != 0:
                    print(action,'  ',state_tuple,'  ',q_value)
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
                
                initial_empty_cells = gamepanel.get_nb_empty_cells()
                initial_state = gamepanel.get_cell_grid()
                
                game2048.gamepanel.move(action)

                new_state = gamepanel.get_cell_grid()
                reward_border = self.reward_largest_tile_on_border(new_state)
                reward_adjacents = self.reward_adjacents_value(new_state)
                reward = reward_border + reward_adjacents + gamepanel.get_nb_empty_cells()
                
                game2048.continue_game()

                next_state = gamepanel.get_cell_grid()
                if action in ['Up', 'Down','Left','Right']:
                    self.update(initial_state, action, reward, next_state)
                    self.update_rotations(initial_state, action, reward, next_state)
                    self.update_double_matrix(initial_state, action, reward, next_state)

                total_reward += reward

            print(f"Épisode {episode + 1}: Récompense totale = {total_reward}")


    def reward_largest_tile_on_border(self,matrix):
        largest_tile = max(max(row) for row in matrix)
        rows, cols = len(matrix), len(matrix[0])

        # Vérifiez si la plus grosse tuile est sur un des 4 bords
        if largest_tile == matrix[0][0] or largest_tile == matrix[0][cols - 1] or largest_tile == matrix[rows - 1][0] or largest_tile == matrix[rows - 1][cols - 1]:
            return 10
        else:
            return 0

    def reward_adjacents_value(self,matrix):
        score = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                if value != 0:
                    # Vérifiez les cases à gauche, en haut, à droite et en bas
                    if j > 0 and matrix[i][j - 1] == value * 2:
                        score += 0.5
                    if i > 0 and matrix[i - 1][j] == value * 2:
                        score += 0.5
                    if j < len(matrix[i]) - 1 and matrix[i][j + 1] == value * 2:
                        score += 0.5
                    if i < len(matrix) - 1 and matrix[i + 1][j] == value * 2:
                        score += 0.5
        return score

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
    
    def update_double_matrix(self,initial_state, action, reward, next_state):
        """Check if there is a 2 in matrix to double 
        However it's an impossible position (every position gets a random cell 2 or 4)
        """
        if any(2 in row for row in initial_state):
            initial_doubled_matrix = tuple(tuple(element * 2 for element in row) for row in initial_state)
            next_doubled_matrix = tuple(tuple(element * 2 for element in row) for row in next_state)
            self.update(initial_doubled_matrix,action,reward,next_doubled_matrix)