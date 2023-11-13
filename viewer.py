from tkinter import *
from classes.Board import Board

def visualize_2048(grid):
    board = Board()
    board.cell_grid = grid
    board.color_grid()
    
    def on_closing():
        board.window.destroy()

    board.window.protocol("WM_DELETE_WINDOW", on_closing)
    board.window.mainloop()

grid = [[8, 512, 256, 32], [2, 16, 64, 0], [2, 16, 8, 0], [4, 2, 0, 0]]

visualize_2048(grid)