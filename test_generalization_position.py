matrix= (
(0, 0, 0, 4) ,
(0, 0, 0, 4) ,
(0, 0, 0, 0),
(0, 0, 4, 8)
)

def extract_tuple_without_zeros(ca):
  """Renvoie un tuple contenant les éléments du tuple d'origine sans les 0."""

  # Créer un tuple avec les éléments du tuple d'origine qui ne sont pas égaux à 0
  return tuple(filter(lambda x: x != 0, ca))


def generate_insertion_possibilities_left_right(tuple_to_insert):

    # Créez un tuple vide de taille 4
    empty_tuple = (0, 0, 0, 0)
    if tuple_to_insert == ():
      return [empty_tuple]
    # Générez toutes les possibilités en utilisant des zéros pour les espaces vides
    possibilities = [empty_tuple[:i] + tuple_to_insert + empty_tuple[i+len(tuple_to_insert):] for i in range(len(empty_tuple) - len(tuple_to_insert) + 1)]

    if len(tuple_to_insert)==2:
       possibilities.append(tuple_to_insert[:1] + (0,0) + tuple_to_insert[1:])
       possibilities.append((0,) + tuple_to_insert[:1] + (0,) + tuple_to_insert[1:])
       possibilities.append( tuple_to_insert[:1] + (0,) + tuple_to_insert[1:] + (0,))
    if len(tuple_to_insert)==3:
       possibilities.append(tuple_to_insert[:1] + (0,) + tuple_to_insert[1:])
       possibilities.append(tuple_to_insert[:2] + (0,) + tuple_to_insert[2:])

    return possibilities

import itertools
def all_possible_positions_left_right(board):
   first_line_possibilities = generate_insertion_possibilities_left_right(extract_tuple_without_zeros(board[0]))
   second_line_possibilities = generate_insertion_possibilities_left_right(extract_tuple_without_zeros(board[1]))
   third_line_possibilities = generate_insertion_possibilities_left_right(extract_tuple_without_zeros(board[2]))
   fourth_line_possibilities = generate_insertion_possibilities_left_right(extract_tuple_without_zeros(board[3]))
    
   # Créer une liste vide pour contenir les combinaisons
   results = []

   # Itérer sur les possibilités de chaque ligne
   for first_line_possibility in first_line_possibilities:
     for second_line_possibility in second_line_possibilities:
       for third_line_possibility in third_line_possibilities:
         for fourth_line_possibility in fourth_line_possibilities:
           # Créer une combinaison avec les possibilités de chaque ligne
           combination = (first_line_possibility, second_line_possibility, third_line_possibility, fourth_line_possibility)

           # Vérifier si la combinaison existe déjà
           if combination not in results:
            # Ajouter la combinaison à la liste
            results.append(combination)
   return results

test = all_possible_positions_left_right(matrix)
# print(test)
print(test)

