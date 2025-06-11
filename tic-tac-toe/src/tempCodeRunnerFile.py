# main.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from game import Game
from renderer import Renderer
from utils import get_best_move  # new function for AI move
import os
import signal
from threading import Timer
import sys
import time # Import time for accurate delays

display_width = 400
display_height = 400

game = None
renderer = None

# Global state variables
in_menu = True
in_ai_choice = False
in_win_screen = False
game_mode = None  # "two_players" or "ai"
human_mark = None
ai_mark = None

# Using GLUT Timer function for better control over animation and state changes
def delayed_action_timer(value):
    global in_win_screen
    if value == 1: # Timer for showing win screen
        in_win_screen = True
        glutPostRedisplay()
    elif value == 2: # Timer for AI's immediate first move if playing as O
        ai_move()
        glutPostRedisplay() # Ensure redraw after AI move

def ai_move():
    global game
    # Ensure AI only moves if it's its turn and game is not over
    if game_mode == "ai" and game.current_player == ai_mark and not game.game_over:
        move = get_best_move(game.board, ai_mark, human_mark)
        if move:
            row, col = move
            game.make_move(row, col)
            # After AI makes a move, check for game over immediately
            if game.game_over:
                handle_game_over()
            glutPostRedisplay() # Request redraw after AI's move

def handle_game_over():
    global in_win_screen, game, renderer
    renderer.win_line_progress = 0.0
    renderer.win_line_start_time = None # Reset win line animation start time

    if game.winner is None: # It's a draw
        in_win_screen = True
        glutPostRedisplay()
    else: # There's a winner, animate win line, then show win screen
        # Use a GLUT timer to show the win screen after the animation duration
        # The animation duration is 1 second in renderer.py (draw_win_line)
        # We need to account for this in our delay.
        glutTimerFunc(1000, delayed_action_timer, 1) # 1000ms = 1 second

def mouse(button, state, x, y):
    global in_menu, in_ai_choice, in_win_screen, game_mode, human_mark, ai_mark
    
    # Convert mouse coordinates to OpenGL Ortho2D coordinates (0-3 for both x and y)
    gl_x = (x / display_width) * 3
    gl_y = ((display_height - y) / display_height) * 3

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if in_menu: # No need for 'not in_ai_choice' here as states are mutually exclusive
            # Main Menu logic
            if 1.0 <= gl_x <= 2.0 and 2.2 <= gl_y <= 2.5: # Two Players Button
                game_mode = "two_players"
                in_menu = False
                game.reset_game() # Reset game for new start
                glutPostRedisplay()
                return
            elif 1.0 <= gl_x <= 2.0 and 1.6 <= gl_y <= 1.9: # Against AI Button
                in_ai_choice = True
                in_menu = False # Transition from menu to AI choice
                glutPostRedisplay()
                return
            elif 1.0 <= gl_x <= 2.0 and 1.0 <= gl_y <= 1.3: # Close Button
                os.kill(os.getpid(), signal.SIGTERM)

        elif in_ai_choice:
            # AI Choice submenu
            if 1.0 <= gl_x <= 2.0 and 2.0 <= gl_y <= 2.3: # Play as X Button
                human_mark = 'X'
                ai_mark = 'O'
                game_mode = "ai"
                in_ai_choice = False
                in_menu = False
                game.reset_game() # Reset game for new start
                glutPostRedisplay()
                return
            elif 1.0 <= gl_x <= 2.0 and 1.4 <= gl_y <= 1.7: # Play as O Button
                human_mark = 'O'
                ai_mark = 'X'
                game_mode = "ai"
                in_ai_choice = False
                in_menu = False
                game.reset_game() # Reset game for new start
                glutPostRedisplay()
                # If human is O, AI starts the game immediately
                glutTimerFunc(500, delayed_action_timer, 2) # 500ms delay for AI to move
                return
            elif 1.0 <= gl_x <= 2.0 and 0.8 <= gl_y <= 1.1: # Exit Button
                os.kill(os.getpid(), signal.SIGTERM)

        elif in_win_screen:
            # Win screen logic
            # Play Again Button: (1.0,1.5)-(2.0,1.8)
            if 1.0 <= gl_x <= 2.0 and 1.5 <= gl_y <= 1.8:
                game.reset_game()
                in_win_screen = False
                glutPostRedisplay()
                # For AI mode, if AI starts, trigger its move
                if game_mode == "ai" and ai_mark == game.current_player:
                    glutTimerFunc(500, delayed_action_timer, 2) # Delay for AI's first move
                return
            # Main Menu Button: (1.0,1.0)-(2.0,1.3)
            elif 1.0 <= gl_x <= 2.0 and 1.0 <= gl_y <= 1.3:
                in_win_screen = False
                in_menu = True
                # Reset game state completely for a fresh start from the main menu
                game.reset_game() 
                # Also reset game mode specific globals
                game_mode = None
                human_mark = None
                ai_mark = None
                glutPostRedisplay()
                return
            # Close Button: (1.0,0.5)-(2.0,0.8)
            elif 1.0 <= gl_x <= 2.0 and 0.5 <= gl_y <= 0.8:
                os.kill(os.getpid(), signal.SIGTERM)

        elif not game.game_over:
            # In game: for two players or AI (human move)
            cell_x = int(gl_x)
            cell_y = int(gl_y)
            
            # For AI mode, only allow move if it is the human turn
            if game_mode == "ai" and game.current_player != human_mark:
                return # Do nothing if it's not the human's turn
            
            game.make_move(cell_y, cell_x)
            
            if game.game_over:
                handle_game_over()
            else: # If game is not over, and it's AI mode, trigger AI's turn
                if game_mode == "ai" and game.current_player == ai_mark:
                    glutTimerFunc(500, delayed_action_timer, 2) # 500ms delay for AI to move
            glutPostRedisplay() # Always redraw after a human move

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if in_menu:
        renderer.draw_menu()
    elif in_ai_choice:
        renderer.draw_ai_choice()
    elif in_win_screen:
        renderer.draw_win_screen()
    else:
        renderer.render()
        # Continuously request redraws while win line animation is active
        if game.game_over and renderer.win_line_progress < 1.0:
            glutPostRedisplay()
    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 3, 0, 3)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    if key == b'r':
        game.reset_game()
        global in_win_screen, in_menu, in_ai_choice, game_mode, human_mark, ai_mark
        in_win_screen = False
        in_menu = True # Go back to main menu on 'r' press
        in_ai_choice = False
        game_mode = None
        human_mark = None
        ai_mark = None
        glutPostRedisplay()

def main():
    global game, renderer
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(display_width, display_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Tic Tac Toe")
    
    glClearColor(0, 0, 0, 1)
    
    game = Game()
    renderer = Renderer(game)
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    
    glutMainLoop()

if __name__ == "__main__":
    main()