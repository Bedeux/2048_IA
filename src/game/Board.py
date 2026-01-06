import numpy as np
from pathlib import Path


class Board:
    __slots__ = ("grid", "lookup_left", "lookup_right", "lookup_score", "rng", "total_score")

    def __init__(self, seed: int | None = None):
        assets_path = Path(__file__).parent / "assets"
        self.lookup_left: np.ndarray = np.load(assets_path / "lookup_left.npy", mmap_mode="r")
        self.lookup_right: np.ndarray = np.load(assets_path / "lookup_right.npy", mmap_mode="r")
        self.lookup_score: np.ndarray = np.load(assets_path / "lookup_score.npy", mmap_mode="r")
        self.rng: np.random.Generator = np.random.default_rng(seed)
        self.grid: np.ndarray = np.zeros((4, 4), dtype=np.int32)  # TODO Voir quoi prendre j'avais avant dtype=np.uint8
        self.total_score = 0
        self.reset()  # Ajout des deux tuiles commme lors de la fin de partie

    def reset(self, start_tiles=2):
        """Réinitialise la grille pour pouvoir simuler une autre partie sans devoir recréer d'objet"""
        self.grid[:] = 0
        # self.total_score = 0
        for _ in range(start_tiles):
            self.add_random_tile()

    def move_left(self) -> np.ndarray:
        """Déplacement vers la gauche"""
        row_scores = self.lookup_score[self.grid[:, 0], self.grid[:, 1], self.grid[:, 2], self.grid[:, 3]]
        self.total_score += np.sum(row_scores)

        self.grid = self.lookup_left[self.grid[:, 0], self.grid[:, 1], self.grid[:, 2], self.grid[:, 3]]
        return self.grid

    def move_right(self) -> np.ndarray:
        """Déplacement vers la droite"""
        row_scores = self.lookup_score[self.grid[:, 0], self.grid[:, 1], self.grid[:, 2], self.grid[:, 3]]
        self.total_score += np.sum(row_scores)

        self.grid = self.lookup_right[self.grid[:, 0], self.grid[:, 1], self.grid[:, 2], self.grid[:, 3]]
        return self.grid

    def move_up(self) -> np.ndarray:
        """Déplacement vers le haut"""
        gT = self.grid.T

        row_scores = self.lookup_score[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.total_score += np.sum(row_scores)

        new_T = self.lookup_left[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.grid = new_T.T
        return self.grid

    def move_down(self) -> np.ndarray:
        """Déplacement vers le bas"""
        gT = self.grid.T

        row_scores = self.lookup_score[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.total_score += np.sum(row_scores)

        new_T = self.lookup_right[gT[:, 0], gT[:, 1], gT[:, 2], gT[:, 3]]
        self.grid = new_T.T
        return self.grid

    def get_score(self) -> int:
        return int(self.total_score)

    def add_random_tile(self) -> np.ndarray:
        """
        Ajoute une nouvelle tuile aléatoire sur une case vide (0) de la grille log2.
        Retourne uniquement la nouvelle grille.
        """
        # Crée un tableau 1D des indices vides
        empty_indices: np.ndarray = np.flatnonzero(self.grid == 0)
        if len(empty_indices) == 0:
            return self.grid  # grille pleine

        # Tirage d'une position aléatoire
        pos: int = int(empty_indices[self.rng.integers(len(empty_indices))])

        # Nouvelle tuile 2 (log2=1) ou 4 (log2=2)
        self.grid.flat[pos] = 1 if self.rng.random() < 0.9 else 2

        return self.grid

    def is_game_over(self) -> bool:
        """
        Vérifie si la partie est terminée pour une grille log2 (uint8).
        Retourne True si plus aucun mouvement possible.
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
        Transforme une grille de puissances de 2 en valeurs réelles.
        Exemple : 1 -> 2, 3 -> 8, etc.
        """
        real_grid = self.grid.astype(np.int32)
        return np.where(real_grid > 0, np.power(2, real_grid), 0)

    def get_max_tile(self):
        """
        Recupere la valeur la valeur de la plus grande tuile
        """
        # TODO refaire sur grid et convertir la plus grande valeur en np power a la place de tout convertir
        return np.max(self.get_real_grid_values())
