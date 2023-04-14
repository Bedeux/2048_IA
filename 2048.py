from tkinter import *
from tkinter import messagebox
import random
import time
from PIL import ImageGrab
from Board import Board

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

        pressedKey = self.best_choice()

        if pressedKey == 'Up':
            self.gamepanel.transpose()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()
            
            
        elif pressedKey == 'Down':
            self.gamepanel.transpose()
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()
            
        elif pressedKey == 'Left':
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()

        elif pressedKey == 'Right':
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
    
        else: 
            pass
        
        self.gamepanel.colorGrid()
        
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
            
        self.gamepanel.colorGrid()
        self.linkKeys(event)
    
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
