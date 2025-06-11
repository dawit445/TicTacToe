class Game:
    def __init__(self):
        self.reset_game()
        self.winning_cells = None

    def make_move(self, row, col):
        if self.game_board[row][col] == ' ' and not self.is_game_finished:
            self.game_board[row][col] = self.active_player
            if self.check_winner():
                # Winning state already set by check_winner
                self.winning_player = self.active_player
            elif self.check_draw():
                self.is_game_finished = True
                self.winning_player = None  # Draw
            else:
                self.active_player = 'red' if self.active_player == 'blue' else 'blue'

    def check_winner(self):
        lines_to_check = [
            # Rows
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # Columns
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # Diagonals
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
        for line in lines_to_check:
            first, second, third = line
            if (self.game_board[first[0]][first[1]] != ' ' and 
                self.game_board[first[0]][first[1]] == self.game_board[second[0]][second[1]] == self.game_board[third[0]][third[1]]):
                self.winning_player = self.game_board[first[0]][first[1]]
                self.is_game_finished = True
                self.winning_cells = (first, third)
                return True
        return False

    def check_draw(self):
        # Draw state: board full and no winner
        return all(cell != ' ' for row in self.game_board for cell in row) and self.winning_player is None

    def reset_game(self):
        self.game_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.active_player = 'blue'  # Blue starts first
        self.is_game_finished = False
        self.winning_player = None
        self.winning_cells = None