class AI_Prioritization:
    def __init__(self, last_move, have_moved):
        self.last_move = last_move
        self.have_moved = have_moved
        self.grid = None
        self.previous_grid = None
        self.availabe_moves = []
        self.empty_cells = -1
        self.max_value_cell = 0

    def best_choice(self):
        if self.last_move is None:
         self.last_move = 'None'
        if self.have_moved is None:
            self.have_moved = True
        if self.have_moved :
            self.last_move = 'Down'
            self.have_moved = False
            return'Down'
        if self.last_move == 'Down' and not self.have_moved:
            self.last_move = 'Left'
            self.have_moved = False
            return'Left'
        if self.last_move == 'Left' and not self.have_moved:
            self.last_move = 'Right'
            self.have_moved = False
            return'Right'
        if self.last_move == 'Right' and not self.have_moved:
            self.last_move = 'Up'
            self.have_moved = False
            return 'Up'
        return 'Down'
