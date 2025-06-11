from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from game import Game
from renderer import Renderer
from utils import calculate_best_move  # Updated function name
import os
import signal
import sys
import time

# Window dimensions
window_width = 600  # Increased for better visibility
window_height = 600

game = None
renderer = None

# Game state variables
show_main_menu = True
show_ai_choice_menu = False
show_win_screen = False
current_game_mode = None  # "two_player" or "ai"
human_color = None
ai_color = None

def delayed_action_timer(value):
    global show_win_screen
    if value == 1:  # Timer for showing win screen
        show_win_screen = True
        glutPostRedisplay()
    elif value == 2:  # Timer for AI's move
        make_ai_move()
        glutPostRedisplay()

def make_ai_move():
    global game
    if (current_game_mode == "ai" and 
        game.active_player == ai_color and 
        not game.is_game_finished):
        
        optimal_move = calculate_best_move(game.game_board, ai_color, human_color)
        if optimal_move:
            row, col = optimal_move
            game.make_move(row, col)
            if game.is_game_finished:
                handle_game_end()
        glutPostRedisplay()

def handle_game_end():
    global show_win_screen, game, renderer
    renderer.winning_animation_progress = 0.0
    renderer.winning_animation_start = None

    if game.winning_player is None:  # Draw
        show_win_screen = True
        glutPostRedisplay()
    else:  # Winner exists, animate winning line
        glutTimerFunc(1000, delayed_action_timer, 1)  # Show win screen after animation

def mouse_click(button, state, x, y):
    global show_main_menu, show_ai_choice_menu, show_win_screen
    global current_game_mode, human_color, ai_color
    
    # Convert to OpenGL coordinates (0-3 range)
    gl_x = (x / window_width) * 3
    gl_y = ((window_height - y) / window_height) * 3

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if show_main_menu:
            handle_main_menu_click(gl_x, gl_y)
        elif show_ai_choice_menu:
            handle_ai_choice_click(gl_x, gl_y)
        elif show_win_screen:
            handle_win_screen_click(gl_x, gl_y)
        else:  # In-game click
            handle_game_click(gl_x, gl_y)

def handle_main_menu_click(x, y):
    global show_main_menu, show_ai_choice_menu, current_game_mode
    # Two Players Button
    if 1.0 <= x <= 2.0 and 2.2 <= y <= 2.5:
        current_game_mode = "two_player"
        show_main_menu = False
        game.reset_game()
    # Against AI Button
    elif 1.0 <= x <= 2.0 and 1.6 <= y <= 1.9:
        show_ai_choice_menu = True
        show_main_menu = False
    # Close Button
    elif 1.0 <= x <= 2.0 and 1.0 <= y <= 1.3:
        exit_game()
    glutPostRedisplay()

def handle_ai_choice_click(x, y):
    global show_ai_choice_menu, current_game_mode, human_color, ai_color
    # Play as Blue Button
    if 1.0 <= x <= 2.0 and 2.0 <= y <= 2.3:
        human_color = 'blue'
        ai_color = 'red'
        current_game_mode = "ai"
        show_ai_choice_menu = False
        game.reset_game()
    # Play as Red Button
    elif 1.0 <= x <= 2.0 and 1.4 <= y <= 1.7:
        human_color = 'red'
        ai_color = 'blue'
        current_game_mode = "ai"
        show_ai_choice_menu = False
        game.reset_game()
        # AI makes first move if playing as blue
        if ai_color == 'blue':
            glutTimerFunc(500, delayed_action_timer, 2)
    # Exit Button
    elif 1.0 <= x <= 2.0 and 0.8 <= y <= 1.1:
        exit_game()
    glutPostRedisplay()

def handle_win_screen_click(x, y):
    global show_win_screen, show_main_menu, current_game_mode, human_color, ai_color
    # Play Again Button
    if 1.0 <= x <= 2.0 and 1.5 <= y <= 1.8:
        game.reset_game()
        show_win_screen = False
        if current_game_mode == "ai" and ai_color == game.active_player:
            glutTimerFunc(500, delayed_action_timer, 2)
    # Main Menu Button
    elif 1.0 <= x <= 2.0 and 1.0 <= y <= 1.3:
        show_win_screen = False
        show_main_menu = True
        game.reset_game()
        current_game_mode = None
        human_color = None
        ai_color = None
    # Close Button
    elif 1.0 <= x <= 2.0 and 0.5 <= y <= 0.8:
        exit_game()
    glutPostRedisplay()

def handle_game_click(x, y):
    if game.is_game_finished:
        return
        
    cell_row = int(y)
    cell_col = int(x)
    
    # For AI mode, only allow human's turn
    if current_game_mode == "ai" and game.active_player != human_color:
        return
        
    game.make_move(cell_row, cell_col)
    
    if game.is_game_finished:
        handle_game_end()
    elif current_game_mode == "ai" and game.active_player == ai_color:
        glutTimerFunc(500, delayed_action_timer, 2)
    glutPostRedisplay()

def exit_game():
    os.kill(os.getpid(), signal.SIGTERM)

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    if show_main_menu:
        renderer.draw_menu()
    elif show_ai_choice_menu:
        renderer.draw_ai_choice()
    elif show_win_screen:
        renderer.draw_win_screen()
    else:
        renderer.render()
        if game.is_game_finished and renderer.winning_animation_progress < 1.0:
            glutPostRedisplay()
    glutSwapBuffers()

def resize_window(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 3, 0, 3)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_input(key, x, y):
    if key == b'r':  # Reset game
        game.reset_game()
        global show_win_screen, show_main_menu, show_ai_choice_menu
        global current_game_mode, human_color, ai_color
        show_win_screen = False
        show_main_menu = True
        show_ai_choice_menu = False
        current_game_mode = None
        human_color = None
        ai_color = None
        glutPostRedisplay()

def initialize_game():
    global game, renderer
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Tic Tac Toe (Blue vs Red)")
    
    glClearColor(0.1, 0.1, 0.15, 1)  # Dark blue-gray background
    
    game = Game()
    renderer = Renderer(game)
    
    glutDisplayFunc(render_scene)
    glutReshapeFunc(resize_window)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard_input)
    
    glutMainLoop()

if __name__ == "__main__":
    initialize_game()