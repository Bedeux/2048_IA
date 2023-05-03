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
        self.gridCell = [[0]*4 for i in range(4)]
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
                self.gridCell[idx][i], self.gridCell[idx][j] = self.gridCell[idx][j], self.gridCell[idx][i]
                i+=1
                j-=1
                
    def transpose(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]
        
    def compressGrid (self):
        self.compress = False
        temp = [[0] * 4 for i in range(4)]
        for i in range(4):
            cnt  =0 
            for j in range(4):
                if self.gridCell[i][j]!=0:
                    temp[i][cnt] = self.gridCell[i][j]
                    if cnt!=j:
                        self.compress = True
                    cnt+=1
        self.gridCell = temp
        
    def mergeGrid(self):
        self.merge = False
        for i in range(4):
            for j in range(4-1):
                if self.gridCell[i][j] == self.gridCell[i][j+1] and self.gridCell[i][j] !=0:
                    self.gridCell[i][j] *=2
                    self.gridCell[i][j+1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True
        
    def randomCell(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    cells.append((i,j))       
        curr = random.choice(cells)
        i = curr[0]
        j = curr[1]
        self.gridCell[i][j]=2
        
    def canMerge(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j+1]:
                    return True
                    
        for i in range(3):
            for j in range(4):
                if self.gridCell[i+1][j] == self.gridCell[i][j]:
                    return True
        return False
        
    def colorGrid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] ==0:
                    self.board[i][j].config(text='', bg = 'azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]), 
                                            bg = self.bgColor.get(str(self.gridCell[i][j])),
                                            fg = self.color.get(str(self.gridCell[i][j])))

    def get_all_random_cells(self):
        cells=[]
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j]==0:
                    cells.append((i,j))       
        return cells

    def get_nb_empty_cells(self):
        empty_cells = 0
        for row in self.gridCell:
            empty_cells += row.count(0)
        return empty_cells