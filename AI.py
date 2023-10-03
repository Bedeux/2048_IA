class AI:
    def __init__(self, game):
        self.game = game
        self.grid = None
        self.previous_grid = None
        self.availabe_moves = []
        self.empty_cells = -1
        self.max_value_cell = 0

    def best_choice(self):
        if self.game.last_move is None:
         self.game.last_move = 'None'
        if self.game.have_moved is None:
            self.game.have_moved = True
        if self.game.have_moved :
            self.game.last_move = 'Down'
            self.game.have_moved = False
            return'Down'
        if self.game.last_move == 'Down' and not self.game.have_moved:
            self.game.last_move = 'Left'
            self.game.have_moved = False
            return'Left'
        if self.game.last_move == 'Left' and not self.game.have_moved:
            self.game.last_move = 'Right'
            self.game.have_moved = False
            return'Right'
        if self.game.last_move == 'Right' and not self.game.have_moved:
            self.game.last_move = 'Up'
            self.game.have_moved = False
            return 'Up'
        return 'Down'

    def AI(self):
        self.update_board_values()
        """
        for possibility in self.availabe_moves:
            score = self.game.gamepanel.get_score_after_move(possibility)
            print(possibility + ": "+str(score))
        print('\n')
        """

    def update_board_values(self):
        self.grid = self.game.gamepanel.get_cell_grid()
        self.previous_grid = self.game.gamepanel.get_previous_grid()
        self.availabe_moves = self.game.gamepanel.get_possible_moves()
        self.empty_cells = self.game.gamepanel.get_nb_empty_cells()
        self.max_value_cell = self.game.gamepanel.get_max_cell_value()
        self.score = self.game.gamepanel.get_score()
