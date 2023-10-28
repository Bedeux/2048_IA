import random
from Board import Board
from Game import Game
from WorstTileGenerator import WorstTileGenerator
import time
import json

class AI_DepthOne:
    def __init__(self, board,weights = {'border': 1.0,'adjacents': 1.0,'future_merges': 1.0,'empty_cells': 1.0}):
        self.board = board
        self.grid = None
        self.previous_grid = None
        self.availabe_moves = []
        self.empty_cells = -1
        self.max_value_cell = 0
        self.score = 0
        self.weights = weights
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
                if reward_action > best_reward and board.different_states(state,next_state):
                    best_reward = reward_action
                    best_action = action
        else :
            best_action = 'None'
        return best_action

    def choose_action_depths(self, board : Board):
        available_moves = board.get_possible_moves()
        if len(available_moves)>0:
            best_action = random.choice(available_moves)
            best_reward = -1
            
            state = board.get_cell_grid()
            for action in available_moves:

                next_state = board.all_grids_next_move[action]
                reward_action = self.get_average_rewards_after_all_possibilities(next_state)
                if reward_action > best_reward and board.different_states(state,next_state):
                    best_reward = reward_action
                    best_action = action
        else :
            best_action = 'None'
        return best_action
    
    def get_average_rewards_after_all_possibilities(self, initial_state, depth=1):
        new_board = Board()
        new_worst_grid = WorstTileGenerator(initial_state)
        new_board.cell_grid = new_worst_grid.get_worst_grid()
        available_moves = new_board.get_possible_moves()
        if len(available_moves)>0:
            reward_actions = []
            for action in available_moves:
                next_state = new_board.all_grids_next_move[action]
                reward_actions.append(self.set_reward(next_state))                
            average_score = round(sum(reward_actions) / len(reward_actions))
            return average_score
        else : 
            return 0

    def update_board_values(self, board):
        self.board = board
        self.grid = board.get_cell_grid()
        self.previous_grid = board.get_previous_grid()
        self.availabe_moves = board.get_possible_moves()
        self.empty_cells = board.get_nb_empty_cells()
        self.max_value_cell = board.get_max_cell_value()
        self.score = board.get_score()

    def set_reward(self,new_state):
        reward_border = self.reward_largest_tile_on_border(new_state) * self.weights['border']
        # reward_adjacents = self.reward_adjacents_value(new_state) * self.weights['adjacents']
        reward_biggest_adjacents = self.reward_two_biggest_adjacent(new_state) * self.weights['biggest_adjacents']
        reward_future_merges = self.reward_tiles_ready_to_converge(new_state) * self.weights['future_merges']
        reward_empty_cells = self.reward_empty_cells(new_state) * self.weights['empty_cells']

        return reward_border + reward_biggest_adjacents + reward_future_merges + reward_empty_cells

    def reward_largest_tile_on_border(self,matrix):
        largest_tile = max(max(row) for row in matrix)
        rows, cols = len(matrix), len(matrix[0])

        # Vérifiez si la plus grosse tuile est sur un des 4 bords
        if largest_tile == matrix[0][0] or largest_tile == matrix[0][cols - 1] or largest_tile == matrix[rows - 1][0] or largest_tile == matrix[rows - 1][cols - 1]:
            return 2
        else:
            return 0

    def reward_adjacents_value(self,matrix):
        """Example : reward += 1 if 4 and 8 are next to"""
        score = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                if value != 0:
                    if j > 0 and matrix[i][j - 1] == value * 2:
                        score += 0.5
                    if i > 0 and matrix[i - 1][j] == value * 2:
                        score += 0.5
                    if j < len(matrix[i]) - 1 and matrix[i][j + 1] == value * 2:
                        score += 0.5
                    if i < len(matrix) - 1 and matrix[i + 1][j] == value * 2:
                        score += 0.5
        return score
    
    def reward_two_biggest_adjacent(self,matrix):
        largest_values = []
        for row in matrix:
            largest_values.extend(row)
        largest_values.sort(reverse=True)

        largest_1, largest_2, largest_3 = largest_values[0], largest_values[1], largest_values[2]
        score = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == largest_1:
                    if (i > 0 and matrix[i - 1][j] == largest_2) or \
                    (i < len(matrix) - 1 and matrix[i + 1][j] == largest_2) or \
                    (j > 0 and matrix[i][j - 1] == largest_2) or \
                    (j < len(matrix[i]) - 1 and matrix[i][j + 1] == largest_2):
                        score += 2

        return score

    def reward_tiles_ready_to_converge(self,matrix):
        """Return the number of pairs that can merge"""
        score = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                value = matrix[i][j]
                if value != 0:
                    if j > 0 and matrix[i][j - 1] == value:
                        score += 0.5
                    if i > 0 and matrix[i - 1][j] == value:
                        score += 0.5
                    if j < len(matrix[i]) - 1 and matrix[i][j + 1] == value:
                        score += 0.5
                    if i < len(matrix) - 1 and matrix[i + 1][j] == value:
                        score += 0.5
        return score

    def reward_empty_cells(self, matrix):
        empty_cells = 0
        for row in matrix:
            empty_cells += row.count(0)
        return empty_cells