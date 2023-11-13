from tkinter import *
import time
from PIL import ImageGrab
from Board import Board

class Game:
    def __init__(self, gamepanel : Board, option_endgame):
        self.gamepanel = gamepanel
        self.option_endgame = option_endgame
        self.end = False
        self.won = False
        self.last_move = 'None'
        self.have_moved = True
        
    def start(self):
       self.gamepanel.random_cell()
       self.gamepanel.random_cell()
       self.gamepanel.color_grid()
    
    def continue_game(self, dipslay_moves = False):
        flag = 0        
        for i in range(4):
            for j in range(4):
                if self.gamepanel.cell_grid[i][j]==0:
                    flag=1
                    break
        if not (flag or self.gamepanel.can_merge()):
            self.end_game(time_sleep=0.5, option=self.option_endgame)
        else :
            if self.gamepanel.moved :
                self.have_moved = True
                self.gamepanel.random_cell()
            
            if dipslay_moves :
                self.gamepanel.color_grid()
                time.sleep(0.2) # Time between each move
                self.gamepanel.window.update_idletasks()
                self.gamepanel.window.update()

    def end_game(self, time_sleep, option= None):
        """
        End the game and perform optional actions.

        Parameters:
        time_sleep : time in seconds waiting with the current window

        option : End the game by specific way
            - 'Score' : print the score of each game in the terminal
            - 'Display': Wait the window displaying and close after time_sleep time.
            - 'Screen': Display the window and screen the board (take_screenshot function)
        """
        self.end = True
        self.gamepanel.color_grid()
        if option=='Score' or option=='Display' or option=='Screen':
            print(str(self.gamepanel.score))
        
        if option=='Display' or option=='Screen':
            # wait the window to appear 
            self.gamepanel.window.update_idletasks()
            self.gamepanel.window.update()
            time.sleep(time_sleep)

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