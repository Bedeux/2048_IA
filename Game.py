from tkinter import *
import time
from PIL import ImageGrab
from Board import Board
from AI import AI

class Game:
    def __init__(self, gamepanel : Board):
        self.gamepanel = gamepanel
        self.end = False
        self.won = False
        self.last_move = 'None'
        self.have_moved = True
        
    def start(self):
       self.gamepanel.random_cell()
       self.gamepanel.random_cell()
       self.gamepanel.color_grid()
       self.gamepanel.window.bind('<Key>', self.linkKeys)
       self.linkKeys("t") # execute link keys without key pressed
       self.gamepanel.window.mainloop()

    def linkKeys(self, event):
        #if game is won or end then simply return
        if self.end or self.won:
            return
        #else
        
        artificial_intelligence = AI(self)
        artificial_intelligence.AI()
        pressedKey = artificial_intelligence.best_choice()
        self.gamepanel.move(pressedKey)
        
        flag = 0        
        for i in range(4):
            for j in range(4):
                if self.gamepanel.cell_grid[i][j]==0:
                    flag=1
                    break
        if not (flag or self.gamepanel.can_merge()):
            self.end_game(time_sleep=3, option='Screen')

        if self.gamepanel.moved:
            self.have_moved = True
            self.gamepanel.random_cell()
            
        self.gamepanel.color_grid()
        self.linkKeys(event)
    
    def end_game(self, time_sleep, option= None):
        """
        End the game and perform optional actions.

        Parameters:
        time_sleep : time in seconds waiting with the current window

        option : End the game by specific way
            - 'Display': Wait the window displaying and close after time_sleep time.
            - 'Screen': Display the window and screen the board (take_screenshot function)
        """
        self.end = True
        print(str(self.gamepanel.score))
        
        if option=='Display' or option=='Screen':
            # wait the window to appear 
            self.gamepanel.window.update_idletasks()
            self.gamepanel.window.update()
            time.sleep(time_sleep)
            self.take_screenshot()

        if option=='Screen':
            self.take_screenshot()
        self.gamepanel.window.after(1, lambda: self.gamepanel.window.destroy())

    def take_screenshot(self):
        x = self.gamepanel.window.winfo_x() + 8
        y = self.gamepanel.window.winfo_y() + 1
        x2 =  x + self.gamepanel.window.winfo_width()
        y2 =  y + self.gamepanel.window.winfo_height() + 30
        screenshot = ImageGrab.grab(bbox=(x,y,x2,y2))
        screenshot.save('./images/'+str(self.gamepanel.score)+'.png')