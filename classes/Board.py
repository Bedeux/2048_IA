from tkinter import *
import random

class Board:
    bgColor = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#f2b179',
        '16': '#f59563',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#edc850',
        '1024': '#edc53f',
        '2048': '#edc22e',
    }

    color = {
        '2': '#776e65',
        '4': '#776e65',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#f9f6f2',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }
    
    def __init__(self):
        self.n=4
        self.window = Tk()
        self.window.title('2048 AI - Bedeux')
        self.gameArea = Frame(self.window, bg = 'azure3')
        self.board = []   
        self.cell_grid = [[0]*4 for i in range(4)]
        self.previous_grid = None
        self.all_grids_next_move = {}
        self.last_moves_action = []
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0
        
        for i in range(4):
            rows = []
            for j in range(4):
                l = Label(self.gameArea, text = '', bg='azure4',
                          font = ('arial',22,'bold'), width=4, height=2)
                l.grid(row = i, column=j, padx=7, pady=7)
                
                rows.append(l)
            self.board.append(rows)
        self.gameArea.grid()
       
    def reverse(self):
        for idx in range(4):
            i = 0
            j=3
            while(i<j):
                self.cell_grid[idx][i], self.cell_grid[idx][j] = self.cell_grid[idx][j], self.cell_grid[idx][i]
                i+=1
                j-=1
                
    def transpose(self):
        self.cell_grid = [list(t) for t in zip(*self.cell_grid)]
        
    def compress_grid (self):
        self.compress = False
        temp = [[0] * 4 for i in range(4)]
        for i in range(4):
            cnt  =0 
            for j in range(4):
                if self.cell_grid[i][j]!=0:
                    temp[i][cnt] = self.cell_grid[i][j]
                    if cnt!=j:
                        self.compress = True
                    cnt+=1
        self.cell_grid = temp

    def move(self, pressed_key):
        self.last_moves_action.append(pressed_key)

        self.all_grids_next_move = {} # Back to zero
        self.previous_grid = self.cell_grid
        if pressed_key == 'Up':
            self.transpose()
            self.compress_grid()
            self.merge_grid()
            self.moved = self.compress or self.merge
            self.compress_grid()
            self.transpose()
            
        elif pressed_key == 'Down':
            self.transpose()
            self.reverse()
            self.compress_grid()
            self.merge_grid()
            self.moved = self.compress or self.merge
            self.compress_grid()
            self.reverse()
            self.transpose()
            
        elif pressed_key == 'Left':
            self.compress_grid()
            self.merge_grid()
            self.moved = self.compress or self.merge
            self.compress_grid()

        elif pressed_key == 'Right':
            self.reverse()
            self.compress_grid()
            self.merge_grid()
            self.moved = self.compress or self.merge
            self.compress_grid()
            self.reverse()

        else: 
            pass

        self.color_grid()

    def move_for_exploration(self, pressed_key):
        if pressed_key == 'Up':
            self.transpose()
            self.compress_grid()
            self.merge_grid()
            self.compress_grid()
            self.transpose()
            
        elif pressed_key == 'Down':
            self.transpose()
            self.reverse()
            self.compress_grid()
            self.merge_grid()
            self.compress_grid()
            self.reverse()
            self.transpose()
            
        elif pressed_key == 'Left':
            self.compress_grid()
            self.merge_grid()
            self.compress_grid()

        elif pressed_key == 'Right':
            self.reverse()
            self.compress_grid()
            self.merge_grid()
            self.compress_grid()
            self.reverse()

        else: 
            pass

        self.color_grid()
        
    def merge_grid(self):
        self.merge = False
        for i in range(4):
            for j in range(4-1):
                if self.cell_grid[i][j] == self.cell_grid[i][j+1] and self.cell_grid[i][j] !=0:
                    self.cell_grid[i][j] *=2
                    self.cell_grid[i][j+1] = 0
                    self.score += self.cell_grid[i][j]
                    self.merge = True
        
    def random_cell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.cell_grid[i][j]==0:
                    cells.append((i,j))       
        curr = random.choice(cells)
        i = curr[0]
        j = curr[1]
        self.cell_grid[i][j]= random.choice([2,4])
        
    def can_merge(self):
        for i in range(4):
            for j in range(3):
                if self.cell_grid[i][j] == self.cell_grid[i][j+1]:
                    return True
                    
        for i in range(3):
            for j in range(4):
                if self.cell_grid[i+1][j] == self.cell_grid[i][j]:
                    return True
        return False
        
    def color_grid(self):
        for i in range(4):
            for j in range(4):
                if self.cell_grid[i][j] ==0:
                    self.board[i][j].config(text='', bg = 'azure4')
                else:
                    self.board[i][j].config(text=str(self.cell_grid[i][j]), 
                                            bg = self.bgColor.get(str(self.cell_grid[i][j])),
                                            fg = self.color.get(str(self.cell_grid[i][j])))

    def get_possible_moves(self):
        moves = []
        for action in ['Left', 'Down', 'Right', 'Up'] :
            state = self.get_cell_grid()
            new_state = self.get_next_state(action)
            if self.different_states(state, new_state):
                moves.append(action)
                self.all_grids_next_move[action] = new_state
        return moves
    
    def different_states(self, state1, state2):
        for i in range(len(state1)):
            for j in range(len(state1[0])):
                if state1[i][j] != state2[i][j]:
                    return True
        return False

    def get_all_random_cells(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.cell_grid[i][j]==0:
                    cells.append((i,j))       
        return cells

    def get_nb_empty_cells(self):
        empty_cells = 0
        for row in self.cell_grid:
            empty_cells += row.count(0)
        return empty_cells
    
    def get_max_cell_value(self):
        max_value = 0
        for row in self.cell_grid:
            for cell in row:
                max_value = max(max_value, cell)
        return max_value
    
    def get_score(self):
        return self.score
    
    def get_cell_grid(self):
        return self.cell_grid

    def get_previous_grid(self):
        return self.previous_grid

    def _backup(self):
        # self._backup_state = (copy.deepcopy(self.cell_grid), self.score)
        self._backup_state = ([list(row) for row in self.cell_grid], self.score)

        
    def _restore(self):
        if self._backup_state is not None:
            self.cell_grid, self.score = self._backup_state
            self._backup_state = None
        
    def get_next_state(self, pressed_key):
        """Return the grid after a specific move (pressed_key)"""
        # Copy the object isn't possible (tkinter error with pickle), creating a new object wasn't performant
        # So I back and restore the object after the move
        self._backup()
        self.move_for_exploration(pressed_key)
        grid = self.cell_grid
        self._restore()
        return grid
    
    def get_score_after_move(self, pressed_key):
        # Copy the object isn't possible (tkinter error with pickle), creating a new object wasn't performant
        # So I back and restore the object after the move
        self._backup()
        self.move_for_exploration(pressed_key)
        score = self.score
        self._restore()
        return score
