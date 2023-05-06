from tkinter import *
import random

class Board:
    bgColor = {
        '2': '#eee4da',
        '4': '#2B89C6',
        '8': '#22CC7E',
        '16':'#E6358B',
        '32':'#CE5404',
        '64':'#F47070',
        '128': '#65A549',
        '256': '#F27C4F',
        '512': '#2ecc72',
        '1024': '#EEC213',
        '2048':'#FF3031',	
        
    }
    color={
         '2': '#0045BE',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
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
        self.cell_grid[i][j]=2
        
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
        rows, cols = len(self.cell_grid), len(self.cell_grid[0])
        for i in range(rows):
            for j in range(cols):
                if self.cell_grid[i][j] == 0:
                    moves = ['Down', 'Left', 'Right', 'Up']
                    return moves
        for i in range(rows):
            for j in range(cols):
                if i > 0 and (self.cell_grid[i][j] == self.cell_grid[i-1][j] or self.cell_grid[i-1][j] == 0) and ('Up' not in moves):
                    moves.append('Up')
                if i < rows - 1 and (self.cell_grid[i][j] == self.cell_grid[i+1][j] or self.cell_grid[i+1][j] == 0) and ('Down' not in moves):
                    moves.append('Down')
                if j > 0 and (self.cell_grid[i][j] == self.cell_grid[i][j-1] or self.cell_grid[i][j-1] == 0) and ('Left' not in moves):
                    moves.append('Left')
                if j < cols - 1 and (self.cell_grid[i][j] == self.cell_grid[i][j+1] or self.cell_grid[i][j+1] == 0) and ('Right' not in moves):
                    moves.append('Right')
        return moves

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
    
    def get_score_after_move(self, pressed_key):
        current_board = self # Create a new instance to keep the original board unchanged
        current_board.move(pressed_key)
        return current_board.score
