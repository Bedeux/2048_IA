import copy
from WorstTileGenerator import WorstTileGenerator

class BoardExploration:
    """Class to explore the next states (with fast execution -> no tkinter)"""
    def __init__(self):
        self.n = 4
        self.cell_grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.all_states = {}
        self.worst_tile_generator = WorstTileGenerator(None)

    def reverse_grid(self, grid):
        reversed_grid = copy.deepcopy(grid)
        for row in reversed_grid:
            row.reverse()
        return reversed_grid

    def transpose_grid(self, grid):
        return [list(t) for t in zip(*grid)]

    def compress_grid(self, grid):
        temp = [[0] * 4 for _ in range(4)]
        for i in range(4):
            cnt = 0
            for j in range(4):
                if grid[i][j] != 0:
                    temp[i][cnt] = grid[i][j]
                    cnt += 1
        return temp

    def merge_grid(self, grid):
        merged_grid = copy.deepcopy(grid)
        for i in range(4):
            for j in range(3):
                if merged_grid[i][j] == merged_grid[i][j + 1] and merged_grid[i][j] != 0:
                    merged_grid[i][j] *= 2
                    merged_grid[i][j + 1] = 0
                    self.score += merged_grid[i][j]
        return merged_grid

    def move(self, grid, pressed_key):
        self.compress = False
        self.merge = False

        if pressed_key == 'Up':
            temp_grid = self.transpose_grid(grid)
            temp_grid = self.compress_grid(temp_grid)
            temp_grid = self.merge_grid(temp_grid)
            temp_grid = self.compress_grid(temp_grid)
            final_grid = self.transpose_grid(temp_grid)
            return final_grid
        elif pressed_key == 'Down':
            temp_grid = self.transpose_grid(grid)
            temp_grid = self.reverse_grid(temp_grid)
            temp_grid = self.compress_grid(temp_grid)
            temp_grid = self.merge_grid(temp_grid)
            temp_grid = self.compress_grid(temp_grid)
            temp_grid = self.reverse_grid(temp_grid)
            final_grid = self.transpose_grid(temp_grid)
            return final_grid
        elif pressed_key == 'Left':
            temp_grid = self.compress_grid(grid)
            temp_grid = self.merge_grid(temp_grid)
            final_grid = self.compress_grid(temp_grid)
            return final_grid
        elif pressed_key == 'Right':
            temp_grid = self.reverse_grid(grid)
            temp_grid = self.compress_grid(temp_grid)
            temp_grid = self.merge_grid(temp_grid)
            temp_grid = self.compress_grid(temp_grid)
            final_grid = self.reverse_grid(temp_grid)
            return final_grid

    def get_possible_moves(self,grid):
        moves = []
        for action in ['Left', 'Down', 'Right', 'Up'] :
            new_state = self.move(grid,action)
            if self.different_states(grid, new_state):
                moves.append(action)
        return moves

    def different_states(self, state1, state2):
        return any(state1[i][j] != state2[i][j] for i in range(4) for j in range(4))

    def get_new_worst_cell(self,grid):
        self.worst_tile_generator.grid = grid
        return self.worst_tile_generator.get_worst_grid()
    
    def get_all_states_depth_one(self, grid):
        all_states = {}
        for action in self.get_possible_moves(grid):
            all_states[action] = self.move(grid,action)
        return all_states

    def get_all_states_depth_three(self, grid):
        all_states = {}

        # First move
        for action in self.get_possible_moves(grid):
            all_states[action] = [self.move(grid,action)]
        
        for initial_action, result_grid in all_states.items():
            result_grid = self.get_new_worst_cell(result_grid[0])
            states = []
            for action in self.get_possible_moves(result_grid):
                states.append(self.move(result_grid,action))
            all_states[initial_action] = states 
        
        for initial_action, result_grid in all_states.items():
            states = []
            for unique_grid in result_grid:
                unique_grid = self.get_new_worst_cell(unique_grid)
                for action in self.get_possible_moves(unique_grid):
                    states.append(self.move(unique_grid,action))
            all_states[initial_action] = states
        
        return all_states
