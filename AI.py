class AI:
    def __init__(self, game):
        self.game = game

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
        for possibility in self.game.gamepanel.get_possible_moves():
            score = self.game.gamepanel.get_score_after_move(possibility)
            print(possibility+": "+str(score))
        print('\n')