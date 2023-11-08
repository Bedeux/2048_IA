from tkinter import *
from Board import Board
import threading

def visualize_2048(grid):
    board = Board()
    board.cell_grid = grid
    board.color_grid()
    
    def on_closing():
        board.window.destroy()

    board.window.protocol("WM_DELETE_WINDOW", on_closing)
    board.window.mainloop()

def display_multiple_grids(grids):
    threads = []

    for grid in grids:
        thread = threading.Thread(target=visualize_2048, args=(grid,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


grids_to_display = [
    [[8, 16, 256, 0], [2, 16, 64, 0], [2, 16, 8, 0], [4, 2, 0, 0]],
    [[0, 0, 16, 256], [0, 4, 8, 64], [4, 8, 16, 8], [2, 2, 4, 2]],
    [[0, 8, 16, 256], [0, 2, 16, 64], [0, 2, 16, 8], [0, 0, 4, 2]]
]

display_multiple_grids(grids_to_display)