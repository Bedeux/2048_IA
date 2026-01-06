from game.Board import Board


def run_demo() -> None:
    """Simple entry point to demonstrate the Board logic."""
    board = Board()

    print("Initial board:")
    print(board.grid)
    board.move_left()
    print(board.grid)
    print(board.get_real_grid_values())


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
