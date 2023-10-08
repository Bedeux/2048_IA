# Matrice d'origine
initial_state = (0, 4, 8, 4), (2, 32, 16, 8), (0, 4, 16, 2), (0, 0, 2, 4)

next_state = (
    (0, 0, 0, 0),
    (0, 0, 0, 2),
    (0, 0, 4, 2),
    (8, 2, 16, 32)
)

def update_rotations(initial_state, action, reward, next_state):
    """Update the Q table with same positions of 2048 pivoted"""
    original_rotated_90 = tuple(zip(*initial_state[::-1]))
    new_rotated_90 = tuple(zip(*next_state[::-1]))
    action_90 = adapt_action(action,90)
    print(original_rotated_90,'  ',new_rotated_90,' ',action_90)

    original_rotated_180 = tuple(tuple(row[::-1]) for row in reversed(initial_state))
    new_rotated_180 = tuple(tuple(row[::-1]) for row in reversed(next_state))
    action_180 = adapt_action(action,180)
    print(original_rotated_180,'  ',new_rotated_180,' ',action_180)

    original_rotated_270 = tuple(tuple(initial_state[j][i] for j in range(len(initial_state))) for i in range(len(initial_state) - 1, -1, -1))
    new_rotated_270 = tuple(tuple(next_state[j][i] for j in range(len(next_state))) for i in range(len(next_state) - 1, -1, -1))
    action_270 = adapt_action(action,270)

    print(original_rotated_270,'  ',new_rotated_270,' ',action_270)
    
def adapt_action(action, degrees):
    action_mapping = {
        "Up": "Right",
        "Down": "Left",
        "Left": "Up",
        "Right": "Down"
    }
    if degrees == 90:
        return action_mapping.get(action, action)
    elif degrees == 180:
        return action_mapping.get(action_mapping.get(action, action), action)
    elif degrees == 270:
        return action_mapping.get(action_mapping.get(action_mapping.get(action, action), action), action)
    else:
        return action  # Initial action


update_rotations(initial_state,"Right",2.0,next_state)