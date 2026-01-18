import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from game.Board import Board


def test_board_initialization():
    board = Board(seed=42)
    assert board.grid.shape == (4, 4)
    assert np.count_nonzero(board.grid) == 2
    assert board.get_score() == 0


def test_reset():
    board = Board(seed=0)
    board.reset()
    assert np.count_nonzero(board.grid) == 2


def test_add_random_tile():
    board = Board(seed=0)
    board.grid[:] = 0
    board.add_random_tile()
    assert np.count_nonzero(board.grid) == 1
    assert np.isin(board.grid[board.grid != 0], [1, 2]).all()


def test_move_left_simple():
    """Test simple de déplacement vers la gauche sur une seule ligne, sans fusion"""
    board = Board()
    board.grid = np.array([[8, 0, 0, 5]], dtype=board.grid.dtype)
    board.move_left()
    expected = np.array([[8, 5, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_left_merge():
    """Test fusion simple de tuiles identiques vers la gauche sur une seule ligne"""
    board = Board()
    board.grid = np.array([[0, 10, 10, 0]], dtype=board.grid.dtype)
    board.move_left()
    expected = np.array([[11, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_left_double_merge():
    """Test double fusion vers la gauche sur une seule ligne"""
    board = Board()
    board.grid = np.array([[13, 13, 13, 13]], dtype=board.grid.dtype)
    board.move_left()
    expected = np.array([[14, 14, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_left_nothing():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[8, 11, 10, 13]], dtype=board.grid.dtype)
    board.move_right()
    expected = np.array([[8, 11, 10, 13]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_right_simple():
    """Test simple de déplacement vers la droite sur une seule ligne, sans fusion"""
    board = Board()
    board.grid = np.array([[0, 12, 0, 5]], dtype=board.grid.dtype)
    board.move_right()
    expected = np.array([[0, 0, 12, 5]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_right_merge():
    """Test fusion simple de tuiles identiques vers la droite sur une seule ligne"""
    board = Board()
    board.grid = np.array([[11, 0, 11, 0]], dtype=board.grid.dtype)
    board.move_right()
    expected = np.array([[0, 0, 0, 12]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_right_double_merge():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[6, 6, 6, 6]], dtype=board.grid.dtype)
    board.move_right()
    expected = np.array([[0, 0, 7, 7]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_right_nothing():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[2, 5, 4, 7]], dtype=board.grid.dtype)
    board.move_right()
    expected = np.array([[2, 5, 4, 7]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_up():
    """Test des déplacements vers le haut (gauche transposée)"""
    board = Board()
    board.grid = np.array([[4, 0, 2, 0], [1, 5, 0, 0], [1, 2, 0, 2], [2, 2, 2, 0]], dtype=board.grid.dtype)
    board.move_up()
    expected = np.array([[4, 5, 3, 2], [2, 3, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_down():
    """Test des déplacements vers le bas (droite transposée)"""
    board = Board()
    board.grid = np.array([[8, 0, 7, 0], [1, 10, 9, 0], [1, 2, 7, 1], [2, 2, 9, 0]], dtype=board.grid.dtype)
    board.move_down()
    expected = np.array([[0, 0, 7, 0], [8, 0, 9, 0], [2, 10, 7, 0], [2, 3, 9, 1]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_get_available_moves():
    """Test des déplacements vers le bas (droite transposée)"""
    board = Board()
    board.grid = np.array([[0, 0, 0, 0], [8, 0, 0, 0], [2, 10, 7, 9], [4, 3, 9, 1]], dtype=board.grid.dtype)
    assert board.get_available_moves_indices() == [0, 3]  # Up + Right


def test_get_available_moves_all():
    """Test des déplacements vers le bas (droite transposée)"""
    board = Board()
    board.grid = np.array([[0, 0, 0, 2], [8, 0, 0, 0], [2, 10, 7, 9], [2, 3, 9, 1]], dtype=board.grid.dtype)
    assert board.get_available_moves_indices() == [0, 1, 2, 3]  # Up + Down + Left + Right


def test_get_available_moves_none():
    """Test des déplacements vers le bas (droite transposée)"""
    board = Board()
    board.grid = np.array([[7, 8, 9, 10], [3, 4, 5, 6], [11, 12, 13, 14], [1, 2, 3, 4]], dtype=board.grid.dtype)
    assert board.get_available_moves_indices() == []


def test_game_over_true():
    board = Board()
    board.grid = np.array([[1, 2, 1, 2], [2, 1, 2, 1], [1, 2, 1, 2], [2, 1, 2, 1]], dtype=board.grid.dtype)
    assert board.is_game_over() is True


def test_game_over_false():
    board = Board()
    board.grid = np.array([[1, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], dtype=board.grid.dtype)
    assert board.is_game_over() is False


def test_get_highest_tile_log2():
    board = Board()
    board.grid = np.array([[1, 2, 3, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], dtype=board.grid.dtype)
    assert board.get_highest_tile_log2() == 4
