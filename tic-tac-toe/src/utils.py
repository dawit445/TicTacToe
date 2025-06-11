def mouse_to_grid(x, y):
    """Convert mouse click coordinates to grid positions."""
    grid_dimension = 3
    cell_width = 200  # Assuming each cell is 200x200 pixels
    grid_col = x // cell_width
    grid_row = y // cell_width
    if 0 <= grid_col < grid_dimension and 0 <= grid_row < grid_dimension:
        return grid_row, grid_col  # Return (row, col) for consistency with board indexing
    return None

def draw_text(text, x, y, color=(1, 1, 0)):
    """Utility function to draw text on the screen with specified color."""
    pass  # Implementation would use OpenGL to render colored text

def reset_game_state():
    """Utility function to reset the game state."""
    return [[' ' for _ in range(3)] for _ in range(3)], 'blue'  # Blue player starts first

# ---------------- Minimax AI functions ------------------
import copy

def evaluate_board(board, ai_color, human_color):
    # Check rows, columns, and diagonals for a win
    winning_lines = [
        # Rows
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        # Columns
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        # Diagonals
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
    ]
    
    for line in winning_lines:
        a, b, c = line
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != ' ':
            if board[a[0]][a[1]] == ai_color:
                return 10  # AI wins
            elif board[a[0]][a[1]] == human_color:
                return -10  # Human wins
    return 0  # No winner yet

def has_available_moves(board):
    for row in board:
        if ' ' in row:
            return True
    return False

def minimax(board, depth, is_maximizing, ai_color, human_color):
    current_score = evaluate_board(board, ai_color, human_color)
    
    # Base cases
    if current_score == 10:  # AI wins
        return current_score - depth  # Prefer faster wins
    if current_score == -10:  # Human wins
        return current_score + depth  # Prefer slower losses
    if not has_available_moves(board):
        return 0  # Draw

    if is_maximizing:  # AI's turn (maximizing player)
        max_eval = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = ai_color
                    evaluation = minimax(board, depth+1, False, ai_color, human_color)
                    board[row][col] = ' '
                    max_eval = max(max_eval, evaluation)
        return max_eval
    else:  # Human's turn (minimizing player)
        min_eval = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = human_color
                    evaluation = minimax(board, depth+1, True, ai_color, human_color)
                    board[row][col] = ' '
                    min_eval = min(min_eval, evaluation)
        return min_eval

def calculate_best_move(board, ai_color, human_color):
    best_value = -float('inf')
    optimal_move = (-1, -1)  # Initialize with invalid move
    board_copy = copy.deepcopy(board)
    
    for row in range(3):
        for col in range(3):
            if board_copy[row][col] == ' ':
                board_copy[row][col] = ai_color
                move_value = minimax(board_copy, 0, False, ai_color, human_color)
                board_copy[row][col] = ' '
                
                if move_value > best_value:
                    best_value = move_value
                    optimal_move = (row, col)
    
    return optimal_move