from tkinter import *
from tkinter import messagebox
import random
import time
from PIL import ImageGrab
from Board import Board

# Recursion limit to 10k
import sys
sys.setrecursionlimit(10000)

class Game:
    def __init__(self, gamepanel):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False
        self.last_move = 'None'
        self.have_moved = True
        
    def start(self):
       self.gamepanel.randomCell()
       self.gamepanel.randomCell()
       self.gamepanel.colorGrid()
       self.gamepanel.window.bind('<Key>', self.linkKeys)
       self.linkKeys("t") # execute link keys without key pressed
       self.gamepanel.window.mainloop()

    def linkKeys(self, event):
        #if game is won or end then simply return
        if self.end or self.won:
            return
        #else
        
        self.AI()
        pressedKey = self.best_choice()
        self.movement(self.gamepanel,pressedKey)
        
        flag = 0        
        for i in range(4):
            for j in range(4):
                if self.gamepanel.gridCell[i][j]==0:
                    flag=1
                    break
        if not (flag or self.gamepanel.canMerge()):
            self.end = True
            print(str(self.gamepanel.score))
            
            # wait the window to appear and takes screenshots
            self.gamepanel.window.update_idletasks()
            self.gamepanel.window.update()
            self.take_screenshot()
            self.gamepanel.window.after(1, lambda: self.gamepanel.window.destroy())

        if self.gamepanel.moved:
            self.have_moved = True
            self.gamepanel.randomCell()
            #print(str(self.gamepanel.gridCell)+"   "+str(self.gamepanel.get_nb_empty_cells())+"    "+str(self.gamepanel.get_all_random_cells())+"   "+str(self.get_possible_moves(self.gamepanel.gridCell)))
            
        self.gamepanel.colorGrid()
        self.linkKeys(event)
    
    def movement(self, gamepanel, pressedKey):
        if pressedKey == 'Up':
            gamepanel.transpose()
            gamepanel.compressGrid()
            gamepanel.mergeGrid()
            gamepanel.moved = gamepanel.compress or gamepanel.merge
            gamepanel.compressGrid()
            gamepanel.transpose()
            
        elif pressedKey == 'Down':
            gamepanel.transpose()
            gamepanel.reverse()
            gamepanel.compressGrid()
            gamepanel.mergeGrid()
            gamepanel.moved = gamepanel.compress or gamepanel.merge
            gamepanel.compressGrid()
            gamepanel.reverse()
            gamepanel.transpose()
            
        elif pressedKey == 'Left':
            gamepanel.compressGrid()
            gamepanel.mergeGrid()
            gamepanel.moved = gamepanel.compress or gamepanel.merge
            gamepanel.compressGrid()

        elif pressedKey == 'Right':
            gamepanel.reverse()
            gamepanel.compressGrid()
            gamepanel.mergeGrid()
            gamepanel.moved = gamepanel.compress or gamepanel.merge
            gamepanel.compressGrid()
            gamepanel.reverse()

        else: 
            pass

        self.gamepanel.colorGrid()

    def best_choice(self):
        if self.last_move is None:
         self.last_move = 'None'
        if self.have_moved is None:
            self.have_moved = True
        if self.have_moved :
            self.last_move = 'Down'
            self.have_moved = False
            return'Down'
        if self.last_move == 'Down' and not self.have_moved:
            self.last_move = 'Left'
            self.have_moved = False
            return'Left'
        if self.last_move == 'Left' and not self.have_moved:
            self.last_move = 'Right'
            self.have_moved = False
            return'Right'
        if self.last_move == 'Right' and not self.have_moved:
            self.last_move = 'Up'
            self.have_moved = False
            return 'Up'
        return 'Down'
    
    def get_possible_moves(self, grid):
        moves = []
        rows, cols = len(grid), len(grid[0])
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    moves = ['Up', 'Down', 'Left', 'Right']
                    return moves
        for i in range(rows):
            for j in range(cols):
                if i > 0 and (grid[i][j] == grid[i-1][j] or grid[i-1][j] == 0) and ('Up' not in moves):
                    moves.append('Up')
                if i < rows - 1 and (grid[i][j] == grid[i+1][j] or grid[i+1][j] == 0) and ('Down' not in moves):
                    moves.append('Down')
                if j > 0 and (grid[i][j] == grid[i][j-1] or grid[i][j-1] == 0) and ('Left' not in moves):
                    moves.append('Left')
                if j < cols - 1 and (grid[i][j] == grid[i][j+1] or grid[i][j+1] == 0) and ('Right' not in moves):
                    moves.append('Right')
        return moves

    def AI(self):
        print("-----------------------------")
        for possibility in self.get_possible_moves(self.gamepanel.gridCell):
            current_board = self.gamepanel
            self.movement(current_board,possibility)
            print(str(current_board.score)+"   "+str(+current_board.get_nb_empty_cells())+"   "+possibility)


    def take_screenshot(self):
        x = self.gamepanel.window.winfo_x() + 8
        y = self.gamepanel.window.winfo_y() + 1
        x2 =  x + self.gamepanel.window.winfo_width()
        y2 =  y + self.gamepanel.window.winfo_height() + 30
        screenshot = ImageGrab.grab(bbox=(x,y,x2,y2))
        screenshot.save('./images/'+str(self.gamepanel.score)+'.png')

start_time = time.time()
n=0
while n<1:
    n+=1
    gamepanel = Board()
    game2048 = Game(gamepanel)
    game2048.start()

print("--- %s seconds ---" % (round(time.time() - start_time,1)))
