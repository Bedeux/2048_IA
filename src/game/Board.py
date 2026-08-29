from pathlib import Path

import numpy as np


class Board:
    """
    Plateau de jeu 2048

    La grille est stockée en représentation log2 :
    0 = case vide, 1 = 2, 2 = 4, 3 = 8, etc
    Ce choix a été fait pour des raisons de performances

    Les déplacements ont été précalculés et stockés dans des 'lookup' pour des raisons de performance
    """

    __slots__ = ("_lookup_left", "_lookup_right", "_lookup_score", "_move_dispatch", "_rng", "grid", "total_score")

    def __init__(self, seed: int | None = None):
        assets_path = Path(__file__).parent / "assets"
        self._lookup_left: np.ndarray = np.load(assets_path / "lookup_left.npy", mmap_mode="r")
        self._lookup_right: np.ndarray = np.load(assets_path / "lookup_right.npy", mmap_mode="r")
        self._lookup_score: np.ndarray = np.load(assets_path / "lookup_score.npy", mmap_mode="r")

        self._rng: np.random.Generator = np.random.default_rng(seed)
        self.grid: np.ndarray = np.zeros((4, 4), dtype=np.uint8)
        self.total_score = 0

        self._move_dispatch = (
            self._move_up,  # 0
            self._move_down,  # 1
            self._move_left,  # 2
            self._move_right,  # 3
        )

        self.reset()  # Ajout des deux tuiles commme lors de la fin de partie

    def clone(self):
        """Clonage optimisé de l'objet courant"""
        b = Board.__new__(Board)
        b._lookup_left = self._lookup_left
        b._lookup_right = self._lookup_right
        b._lookup_score = self._lookup_score
        b.grid = self.grid.copy()
        b.total_score = self.total_score
        b._move_dispatch = (b._move_up, b._move_down, b._move_left, b._move_right)
        b._rng = np.random.default_rng(self._rng.integers(2**63))
        return b

    def reset(self, start_tiles=2):
        """Réinitialise la grille pour pouvoir simuler une autre partie sans devoir recréer d'objet"""
        self.grid[:] = 0
        self.total_score = 0
        for _ in range(start_tiles):
            self._add_random_tile()

    def _move_left(self):
        """Déplacement vers la gauche"""
        g = self.grid
        row_scores = self._lookup_score[g[:, 0], g[:, 1], g[:, 2], g[:, 3]]
        self.total_score += np.sum(row_scores)
        self.grid = self._lookup_left[g[:, 0], g[:, 1], g[:, 2], g[:, 3]]

    def _move_right(self):
        """Déplacement vers la droite"""
        g = self.grid
        row_scores = self._lookup_score[g[:, 0], g[:, 1], g[:, 2], g[:, 3]]
        self.total_score += np.sum(row_scores)
        self.grid = self._lookup_right[g[:, 0], g[:, 1], g[:, 2], g[:, 3]]

    def _move_up(self):
        """Déplacement vers le haut"""
        gT = self.grid.T
        row_scores = self._lookup_score[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.total_score += np.sum(row_scores)
        self.grid = self._lookup_left[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]].T

    def _move_down(self):
        """Déplacement vers le bas"""
        gT = self.grid.T
        row_scores = self._lookup_score[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.total_score += np.sum(row_scores)
        self.grid = self._lookup_right[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]].T

    def move(self, direction: int):
        """
        Applique un déplacement sur le plateau en fonction de la direction fournie
        La direction est codée sous forme d'entier : 0=up, 1=down, 2=left, 3=right

        Après l'application du déplacement, une nouvelle tuile aléatoire est ajoutée à la grille

        Attention
        ---------
        Pour des raisons de performance, cette méthode ne vérifie pas si le plateau a réellement
        changé avant d'ajouter la nouvelle tuile
        L'utilisation préalable de la méthode `get_available_moves_indices()` est donc recommandé
        afin d'identifier en amont les déplacements valides
        """
        self._move_dispatch[direction]()
        self._add_random_tile()

    def get_score(self) -> int:
        return int(self.total_score)

    def _add_random_tile(self) -> np.ndarray:
        """
        Ajoute une nouvelle tuile aléatoire sur une case vide (0) de la grille log2
        Retourne uniquement la nouvelle grille
        """
        # Crée un tableau 1D des indices vides
        empty_indices: np.ndarray = np.flatnonzero(self.grid == 0)
        if len(empty_indices) == 0:
            return self.grid  # grille pleine

        # Tirage d'une position aléatoire
        pos: int = int(empty_indices[self._rng.integers(len(empty_indices))])

        # Nouvelle tuile 2 (log2=1) ou 4 (log2=2)
        self.grid.flat[pos] = 1 if self._rng.random() < 0.9 else 2

        return self.grid

    def get_available_moves_indices(self):
        """
        Retourne une liste avec les indices des mouvements possibles :
        0=up, 1=down, 2=left, 3=right
        Fonction proposé par ChatGPT (plus performante)
        """
        moves = []
        dirs = [
            (self._lookup_left, True, 0),  # UP
            (self._lookup_right, True, 1),  # DOWN
            (self._lookup_left, False, 2),  # LEFT
            (self._lookup_right, False, 3),  # RIGHT
        ]

        for lookup, is_col, idx in dirs:
            for i in range(4):
                line = self.grid[:, i] if is_col else self.grid[i, :]
                lkup = lookup[line[0], line[1], line[2], line[3]]
                if any(line[j] != lkup[j] for j in range(4)):
                    moves.append(idx)
                    break

        return moves

    def is_game_over(self) -> bool:
        """
        Vérifie si la partie est terminée
        Retourne True si aucun mouvement n'est possible
        """
        g: np.ndarray = self.grid

        # S'il reste une case vide → pas game over
        if np.any(g == 0):
            return False

        # Vérifie les fusions possibles horizontalement
        if np.any(g[:, :-1] == g[:, 1:]):
            return False

        # Vérifie les fusions possibles verticalement
        if np.any(g[:-1, :] == g[1:, :]):
            return False

        # Aucune case vide ni fusion possible → game over
        return True

    def get_real_grid_values(self):
        """
        Fonction d'exploration permettant de transforme la grille log2 en valeurs réelles
        Exemple : 1 -> 2, 3 -> 8, etc.
        Cela permet d'avoir un apercu de la vraie grille
        """
        real_grid = self.grid.astype(np.int32)
        return np.where(real_grid > 0, np.power(2, real_grid), 0)

    def get_highest_tile_log2(self):
        """
        Recupere la valeur de la plus grande tuile
        """
        return int(self.grid.max())
