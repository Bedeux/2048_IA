import numpy as np

def move_left_line(line):
    """
    Déplace et fusionne une ligne vers la gauche.
    Entrée : liste ou array de 4 éléments log2
    Retour : (np.array de 4 éléments log2, score gagné)
    """
    line = [x for x in line if x != 0]  # enlève les zéros
    merged = []
    score = 0
    skip = False
    for i in range(len(line)):
        if skip:
            skip = False
            continue
        if i + 1 < len(line) and line[i] == line[i + 1]:
            new_val = line[i] + 1  # fusion (ex: 1+1 -> 2)
            merged.append(new_val)
            score += 2 ** new_val   # score officiel du 2048
            skip = True
        else:
            merged.append(line[i])

    # Complète avec des zéros
    merged += [0] * (4 - len(merged))
    return np.array(merged, dtype=np.uint8), score


def move_right_line(line):
    """
    Déplace et fusionne une ligne vers la droite (en inversant avant/après)
    Retourne (np.array de 4 éléments log2, score)
    """
    reversed_line = list(reversed(line))
    new_line, score = move_left_line(reversed_line)
    return np.array(list(reversed(new_line)), dtype=np.uint8), score


def build_lookup_table_left():
    """
    Construit les lookup tables pour toutes les lignes possibles (4 cases log2 : 0..16)
    Retourne :
        - lookup_tiles : np.ndarray[(17,17,17,17,4), dtype=np.uint8]
        - lookup_score : np.ndarray[(17,17,17,17), dtype=np.uint32]
    """
    lookup_tiles = np.zeros((17, 17, 17, 17, 4), dtype=np.uint8)
    lookup_score = np.zeros((17, 17, 17, 17), dtype=np.uint32)

    for a in range(17):
        for b in range(17):
            for c in range(17):
                for d in range(17):
                    line = [a, b, c, d]
                    new_line, score = move_left_line(line)
                    lookup_tiles[a, b, c, d] = new_line
                    lookup_score[a, b, c, d] = score

    return lookup_tiles, lookup_score


def build_lookup_table_right():
    """
    Construit les lookup tables pour move right (lignes 4 cases log2 : 0..16)
    Retourne :
        - lookup_tiles : np.ndarray[(17,17,17,17,4), dtype=np.uint8]
        - lookup_score : np.ndarray[(17,17,17,17), dtype=np.uint32]
    """
    lookup_tiles = np.zeros((17, 17, 17, 17, 4), dtype=np.uint8)
    lookup_score = np.zeros((17, 17, 17, 17), dtype=np.uint32)

    for a in range(17):
        for b in range(17):
            for c in range(17):
                for d in range(17):
                    line = [a, b, c, d]
                    new_line, score = move_right_line(line)
                    lookup_tiles[a, b, c, d] = new_line
                    lookup_score[a, b, c, d] = score

    return lookup_tiles, lookup_score

lookup_left_tiles, lookup_left_score = build_lookup_table_left()
lookup_right_tiles, lookup_right_score = build_lookup_table_right()

np.save("lookup_left.npy", lookup_left_tiles)
np.save("lookup_right.npy", lookup_right_tiles)

np.save("lookup_score.npy", lookup_left_score) # on garde une seule lookup car qu'on aille à droite ou à gauche, le même score sera obtenu

