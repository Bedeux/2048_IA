import numpy as np

from game.Board import Board


def run_demo() -> None:
    """Simple entry point to demonstrate the Board logic."""
    board = Board(seed=54)

    board.move(1)
    board.move(3)
    board.move(3)
    board.move(1)

    print("Exemple grille après quelques déplacements")
    print(board.grid)


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
