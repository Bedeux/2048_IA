import random
import copy

class WorstTileGenerator:
    def __init__(self, grid):
        self.grid = grid

    def get_all_empty_cells(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.grid[i][j]==0:
                    cells.append((i,j))                  
        return cells
    
    def get_all_random_positions(self):
        all_random_positions = []
        for tile in self.get_all_empty_cells():
            temp_grid = copy.deepcopy(self.grid)
            temp_grid[tile[0]][tile[1]]= 2
            all_random_positions.append(temp_grid)
            temp_grid = copy.deepcopy(self.grid)
            temp_grid[tile[0]][tile[1]]= 4
            all_random_positions.append(temp_grid)
        return all_random_positions

            
    def score_for_full_lines_and_columns(self, grid):
        score = 0
        
        for row in grid:
            if 0 not in row:
                score += 2

        for col in range(len(grid)):
            if all(grid[row][col] != 0 for row in range(len(grid))):
                score += 2
        return score
    
    def reward_tiles_ready_to_converge(self, grid):
        """Return the number of pairs that can merge"""
        score = 0

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                value = grid[i][j]
                if value != 0:
                    # adjacents
                    if j > 0 and grid[i][j - 1] == value:
                        score -= 1
                    if i > 0 and grid[i - 1][j] == value:
                        score -= 1

                    # with zeros between (left-right)
                    left = j - 1
                    while left >= 0 and grid[i][left] == 0:
                        left -= 1
                    if left >= 0 and grid[i][left] == value:
                        score -= 1

                    # with zeros between (up-down)
                    up = i - 1
                    while up >= 0 and grid[up][j] == 0:
                        up -= 1
                    if up >= 0 and grid[up][j] == value:
                        score -= 1
        return score

    
    def get_reward(self, grid):
        reward_score = self.score_for_full_lines_and_columns(grid)
        reward_minimum_merges = self.reward_tiles_ready_to_converge(grid)
        return reward_score + reward_minimum_merges
    
    def get_worst_grid(self):
        position_rewards = {}
        for position in self.get_all_random_positions():
            position_rewards[str(position)] = self.get_reward(position)
        best_positions = [pos for pos, score in position_rewards.items() if score == max(position_rewards.values())]
        if len(best_positions)>0:
            best_position_str = random.choice(best_positions)  # If max score on different positions
            best_grid = eval(best_position_str) # str to list
        else : 
            best_grid = self.grid
        return best_grid