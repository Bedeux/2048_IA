import random
from Board import Board
from BoardExploration import BoardExploration

class AI_DepthOne:
    def __init__(self,weights = {'border': 1.0,'adjacents':1.0,'biggest_adjacents': 1.0,'future_merges': 1.0,'empty_cells': 1.0, 'full_line':1.0 }):
        self.weights = weights
        self.temp_board = BoardExploration()
        
    def choose_action(self, board : Board):
        state = board.get_cell_grid()
        new_states = self.temp_board.get_all_states_depth_one(state)
        if len(new_states)>0:
            best_action = random.choice(list(new_states.keys()))
            best_reward = -1000
            for action, new_state in new_states.items():
                reward_action = self.set_reward(new_state)
                if reward_action > best_reward and board.different_states(state,new_state):
                    best_reward = reward_action
                    best_action = action
        else :
            best_action = 'None'
        return best_action
    
    def choose_action_depths(self, board : Board):
        """TEST : AI on depth 3"""
        all_states = self.temp_board.get_all_states_depth_three(board.cell_grid)
        best_action = random.choice(['Up','Down','Left','Right'])

        action_best_reward = {'Up':-100,'Down':-100,'Left':-100,'Right':-100}
        for action,grids in all_states.items():
            for grid in grids:
                reward = self.set_reward(grid)
                if float(reward) > float(action_best_reward[action]):
                    action_best_reward[action] = reward
        
        best_action = max(action_best_reward, key= lambda x: action_best_reward[x])
        return best_action

    def set_reward(self,new_state):
        reward_border = self.reward_largest_tile_on_border(new_state) * self.weights['border']
        # reward_adjacents = self.reward_adjacents_value(new_state) * self.weights['adjacents']
        reward_biggest_adjacents = self.reward_two_biggest_adjacent(new_state) * self.weights['biggest_adjacents']
        reward_future_merges = self.reward_tiles_ready_to_converge(new_state) * self.weights['future_merges']
        reward_empty_cells = self.reward_empty_cells(new_state) * self.weights['empty_cells']
        reward_full_line = self.reward_full_line_with_largest_tile(new_state) * self.weights['full_line']
        reward_weight_sum = self.reward_weighted_sum_of_tiles(new_state)* self.weights['weighted_sum']
        return reward_border + reward_biggest_adjacents + reward_future_merges + reward_empty_cells + reward_full_line + reward_weight_sum

    def reward_largest_tile_on_border(self, matrix):
        largest_tile = max(max(row) for row in matrix)
        rows, cols = len(matrix), len(matrix[0])

        # Check whether the largest tile is on one of the board's corners
        if largest_tile == matrix[0][0] or largest_tile == matrix[0][cols - 1] or largest_tile == matrix[rows - 1][0] or largest_tile == matrix[rows - 1][cols - 1]:
            return 2
        # Check whether the largest tile is in one of the first rows, last rows, first columns or last columns.    
        elif largest_tile in matrix[0] or largest_tile in matrix[rows - 1] or largest_tile in [row[0] for row in matrix] or largest_tile in [row[cols - 1] for row in matrix]:
            return 1
        else:
            return 0 # if the largest tile in the middle of the board
    
    def reward_full_line_with_largest_tile(self, matrix):
        """Reward when the main line or column of the largest tile isn't empty"""
        largest_tile = max(max(row) for row in matrix)
        rows, cols = len(matrix), len(matrix[0])

        # Check whether the largest tile is on one of the board's corners
        if largest_tile == matrix[0][0] or largest_tile == matrix[0][cols - 1] or largest_tile == matrix[rows - 1][0] or largest_tile == matrix[rows - 1][cols - 1]:
            # get line and column index of largest tile
            for i in range(rows):
                for j in range(cols):
                    if matrix[i][j] == largest_tile:
                        row_with_largest_tile = i
                        column_with_largest_tile = j

            row_sum = sum(matrix[row_with_largest_tile])
            column_sum = sum(matrix[i][column_with_largest_tile] for i in range(rows))

            # Check that there are no empty cells (i.e. no zeros) in the row or column with the largest cells
            if all(matrix[row_with_largest_tile]) and row_sum>=column_sum:
                return 1  
            if all(matrix[i][column_with_largest_tile] for i in range(rows)) and column_sum>row_sum:
                return 1  
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
                value_coef = 1 
                if value<=128:
                    value_coef=0.9 # Less coeff if low value
                if value != 0:
                    if j > 0 and matrix[i][j - 1] == value:
                        score += 0.5*value_coef
                    if i > 0 and matrix[i - 1][j] == value:
                        score += 0.5*value_coef
                    if j < len(matrix[i]) - 1 and matrix[i][j + 1] == value:
                        score += 0.5*value_coef
                    if i < len(matrix) - 1 and matrix[i + 1][j] == value:
                        score += 0.5*value_coef
        return score
    
    def reward_weighted_sum_of_tiles(self,matrix):
        largest_tile = max(max(row) for row in matrix)
        rows, cols = len(matrix), len(matrix[0])

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == largest_tile:
                    row_with_largest_tile = i
                    column_with_largest_tile = j

        total_reward = 0
        for i in range(rows):
            for j in range(cols):
                tile = matrix[i][j]
                if tile > 0:
                    distance = abs(i - row_with_largest_tile) + abs(j - column_with_largest_tile)
                    if distance == 0:
                        coefficient = 2
                    else:
                        coefficient = 1 / distance  
                    total_reward += tile * coefficient
        return total_reward/largest_tile

    def reward_empty_cells(self, matrix):
        empty_cells = 0
        for row in matrix:
            empty_cells += row.count(0)
        return empty_cells