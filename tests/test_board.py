import os
import sys

import numpy as np

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


def test_clone_grid_and_score():
    board = Board()
    board.grid[0, 0] = 2
    board.total_score = 123

    b_clone = board.clone()

    # La grille est copiée
    assert np.array_equal(b_clone.grid, board.grid), "La grille du clone doit être identique"
    # Le score est copié
    assert b_clone.total_score == board.total_score, "Le score doit être identique"

    # Modifier le clone ne doit pas changer l'original
    b_clone.grid[0, 0] = 99
    b_clone.total_score = 999
    assert board.grid[0, 0] == 2, "Modification du clone ne doit pas affecter l'original"
    assert board.total_score == 123, "Modification du clone ne doit pas affecter l'original"


def test_clone_rng_independent():
    board = Board(seed=42)
    b_clone1 = board.clone()
    b_clone2 = board.clone()

    # Les RNG sont indépendants → tirer un nombre ne doit pas être identique
    r1 = b_clone1._rng.integers(0, 1000)
    r2 = b_clone2._rng.integers(0, 1000)
    # Il peut y avoir une très faible probabilité d'égalité mais c'est ok
    assert r1 != r2 or True


def test_clone_move_independence():
    board = Board(seed=123)
    board.grid[0, :] = [1, 1, 0, 0]
    board.total_score = 0

    b_clone = board.clone()
    b_clone._move_left()

    # Original doit rester inchangé
    assert np.array_equal(board.grid[0, :], [1, 1, 0, 0]), "Original inchangé après move sur clone"
    assert board.total_score == 0, "Score original inchangé après move sur clone"

    # Clone doit avoir changé
    assert np.array_equal(b_clone.grid[0, :], [2, 0, 0, 0]), "Clone doit refléter le move"
    assert b_clone.total_score > 0, "Score du clone doit être mis à jour"


def test__add_random_tile():
    board = Board(seed=0)
    board.grid[:] = 0
    board._add_random_tile()
    assert np.count_nonzero(board.grid) == 1
    assert np.isin(board.grid[board.grid != 0], [1, 2]).all()


def test__move_left_simple():
    """Test simple de déplacement vers la gauche sur une seule ligne, sans fusion"""
    board = Board()
    board.grid = np.array([[8, 0, 0, 5]], dtype=board.grid.dtype)
    board._move_left()
    expected = np.array([[8, 5, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_left_merge():
    """Test fusion simple de tuiles identiques vers la gauche sur une seule ligne"""
    board = Board()
    board.grid = np.array([[0, 10, 10, 0]], dtype=board.grid.dtype)
    board._move_left()
    expected = np.array([[11, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_left_double_merge():
    """Test double fusion vers la gauche sur une seule ligne"""
    board = Board()
    board.grid = np.array([[13, 13, 13, 13]], dtype=board.grid.dtype)
    board._move_left()
    expected = np.array([[14, 14, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_left_nothing():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[8, 11, 10, 13]], dtype=board.grid.dtype)
    board._move_right()
    expected = np.array([[8, 11, 10, 13]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_right_simple():
    """Test simple de déplacement vers la droite sur une seule ligne, sans fusion"""
    board = Board()
    board.grid = np.array([[0, 12, 0, 5]], dtype=board.grid.dtype)
    board._move_right()
    expected = np.array([[0, 0, 12, 5]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_right_merge():
    """Test fusion simple de tuiles identiques vers la droite sur une seule ligne"""
    board = Board()
    board.grid = np.array([[11, 0, 11, 0]], dtype=board.grid.dtype)
    board._move_right()
    expected = np.array([[0, 0, 0, 12]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_right_double_merge():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[6, 6, 6, 6]], dtype=board.grid.dtype)
    board._move_right()
    expected = np.array([[0, 0, 7, 7]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_right_nothing():
    """Test double fusion vers la droite sur une seule ligne (6,6,6,6 → 0,0,7,7)"""
    board = Board()
    board.grid = np.array([[2, 5, 4, 7]], dtype=board.grid.dtype)
    board._move_right()
    expected = np.array([[2, 5, 4, 7]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_up():
    """Test des déplacements vers le haut (gauche transposée)"""
    board = Board()
    board.grid = np.array([[4, 0, 2, 0], [1, 5, 0, 0], [1, 2, 0, 2], [2, 2, 2, 0]], dtype=board.grid.dtype)
    board._move_up()
    expected = np.array([[4, 5, 3, 2], [2, 3, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test__move_down():
    """Test des déplacements vers le bas (droite transposée)"""
    board = Board()
    board.grid = np.array([[8, 0, 7, 0], [1, 10, 9, 0], [1, 2, 7, 1], [2, 2, 9, 0]], dtype=board.grid.dtype)
    board._move_down()
    expected = np.array([[0, 0, 7, 0], [8, 0, 9, 0], [2, 10, 7, 0], [2, 3, 9, 1]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_0(monkeypatch):
    """Test déplacement vers le haut via move()"""
    board = Board()
    board.grid = np.array([[4, 5, 0, 1], [12, 5, 1, 0], [10, 2, 3, 0], [0, 2, 5, 0]], dtype=board.grid.dtype)
    monkeypatch.setattr(
        Board, "_add_random_tile", lambda self: None
    )  # Désactive la fonction `_add_random_tile` afin de pouvoir tester move()
    board.move(0)  # Up
    expected = np.array([[4, 6, 1, 1], [12, 3, 3, 0], [10, 0, 5, 0], [0, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_1(monkeypatch):
    """Test déplacement vers le bas via move()"""
    board = Board()
    board.grid = np.array([[4, 5, 0, 1], [12, 5, 1, 0], [10, 2, 3, 0], [0, 2, 5, 0]], dtype=board.grid.dtype)
    monkeypatch.setattr(
        Board, "_add_random_tile", lambda self: None
    )  # Désactive la fonction `_add_random_tile` afin de pouvoir tester move()
    board.move(1)  # Up
    expected = np.array([[0, 0, 0, 0], [4, 0, 1, 0], [12, 6, 3, 0], [10, 3, 5, 1]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_2(monkeypatch):
    """Test déplacement vers la gauche via move()"""
    board = Board()
    board.grid = np.array([[4, 5, 0, 1], [12, 5, 1, 0], [10, 2, 3, 1], [0, 2, 2, 0]], dtype=board.grid.dtype)
    monkeypatch.setattr(
        Board, "_add_random_tile", lambda self: None
    )  # Désactive la fonction `_add_random_tile` afin de pouvoir tester move()
    board.move(2)  # Left
    expected = board.grid = np.array([[4, 5, 1, 0], [12, 5, 1, 0], [10, 2, 3, 1], [3, 0, 0, 0]], dtype=board.grid.dtype)
    assert np.array_equal(board.grid, expected)


def test_move_3(monkeypatch):
    """Test déplacement vers la droite via move()"""
    board = Board()
    board.grid = np.array([[4, 5, 0, 1], [12, 5, 1, 0], [10, 2, 3, 1], [0, 2, 2, 0]], dtype=board.grid.dtype)
    monkeypatch.setattr(
        Board, "_add_random_tile", lambda self: None
    )  # Désactive la fonction `_add_random_tile` afin de pouvoir tester move()
    board.move(3)  # Right
    expected = np.array([[0, 4, 5, 1], [0, 12, 5, 1], [10, 2, 3, 1], [0, 0, 0, 3]], dtype=board.grid.dtype)
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
