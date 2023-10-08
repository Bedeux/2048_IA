import random
from Board import Board
from Game import Game
import time
import json

class RLAgentSimplified:
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

    def choose_action(self, board : Board):
        available_moves = board.get_possible_moves()
        # print(available_moves)
        if len(available_moves)>0:
            best_action = random.choice(available_moves)
            best_reward = -1
            
            state = board.get_cell_grid()
            
            for action in available_moves:
                next_state = board.all_grids_next_move[action]
                reward_action = self.set_reward(next_state)
                print(state,'  ',action,'  ',next_state,'  ',reward_action)
                if reward_action > best_reward:
                    
                    best_reward = reward_action
                    best_action = action
                    return best_action
        else :
            best_action = 'None'
        print(best_action)
        return best_action

    def update_board_values(self, board):
        self.board = board
        self.grid = board.get_cell_grid()
        self.previous_grid = board.get_previous_grid()
        self.availabe_moves = board.get_possible_moves()
        self.empty_cells = board.get_nb_empty_cells()
        self.max_value_cell = board.get_max_cell_value()
        self.score = board.get_score()

    def set_reward(self,new_state):
        reward_border = self.reward_largest_tile_on_border(new_state)
        reward_adjacents = self.reward_adjacents_value(new_state)
        reward_empty_cells = self.reward_empty_cells(new_state)
        return reward_border + reward_adjacents + reward_empty_cells

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
    
    def reward_empty_cells(self, matrix):
        empty_cells = 0
        for row in matrix:
            empty_cells += row.count(0)
        return empty_cells