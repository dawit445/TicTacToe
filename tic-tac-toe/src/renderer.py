from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time

def draw_text(text, x, y, color=(1, 1, 0)):  
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

class Renderer:
    def __init__(self, game):
        self.game = game
        self.winning_animation_progress = 0.0  
        self.winning_animation_start = None

    def draw_grid(self):
        glColor3f(0.5, 0.5, 0.5)  # Gray grid lines
        glBegin(GL_LINES)
        for i in range(1, 3):
            glVertex2f(i, 0)
            glVertex2f(i, 3)
            glVertex2f(0, i)
            glVertex2f(3, i)
        glEnd()

    def draw_marks(self):
        for row in range(3):
            for col in range(3):
                player_color = self.game.game_board[row][col]
                if player_color != ' ':
                    center_x = col + 0.5
                    center_y = row + 0.5
                    self.draw_player_mark(player_color, center_x, center_y)

    def draw_player_mark(self, player_color, x, y):
        if player_color == 'blue':
            glColor3f(0.2, 0.4, 1.0)  # Bright blue
            glBegin(GL_LINES)
            glVertex2f(x - 0.3, y - 0.3)
            glVertex2f(x + 0.3, y + 0.3)
            glVertex2f(x - 0.3, y + 0.3)
            glVertex2f(x + 0.3, y - 0.3)
            glEnd()
        elif player_color == 'red':
            glColor3f(1.0, 0.3, 0.3)  # Bright red
            num_segments = 50
            glBegin(GL_LINE_LOOP)
            for i in range(num_segments):
                theta = 2.0 * np.pi * i / num_segments
                dx = 0.3 * np.cos(theta)
                dy = 0.3 * np.sin(theta)
                glVertex2f(x + dx, y + dy)
            glEnd()
    
    def draw_winning_line(self):
        if not self.game.winning_cells or len(self.game.winning_cells) < 2:
            return

        if self.winning_animation_start is None:
            self.winning_animation_start = time.time()

        # Animate for 1 second
        elapsed = time.time() - self.winning_animation_start
        animation_duration = 1  # Match with glutTimerFunc delay
        progress = min(elapsed / animation_duration, 1.0)
        self.winning_animation_progress = progress

        start_cell = self.game.winning_cells[0]
        end_cell = self.game.winning_cells[1]

        def get_cell_center(cell):
            return (cell[1] + 0.5, cell[0] + 0.5)

        start_pos = get_cell_center(start_cell)
        end_pos = get_cell_center(end_cell)

        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * self.winning_animation_progress
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * self.winning_animation_progress

        glColor3f(1.0, 1.0, 0.0)  # Yellow winning line
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex2f(*start_pos)
        glVertex2f(current_x, current_y)
        glEnd()

    def render(self):
        self.draw_grid()
        self.draw_marks()
        if self.game.is_game_finished:
            self.draw_winning_line()

    def draw_menu(self):
        # Draw background
        glColor3f(0.15, 0.15, 0.2)  # Dark blue-gray background
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(3, 0)
        glVertex2f(3, 3)
        glVertex2f(0, 3)
        glEnd()

        # Title
        draw_text("TIC TAC TOE", 0.9, 2.6, (0.9, 0.9, 1.0))  # Light blue text

        # Two Players Button
        glColor3f(0.3, 0.6, 0.3)  # Green button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 2.2)
        glVertex2f(2.0, 2.2)
        glVertex2f(2.0, 2.5)
        glVertex2f(1.0, 2.5)
        glEnd()
        draw_text("Two Players", 1.1, 2.35, (0, 0, 0))  # Black text

        # Against AI Button
        glColor3f(0.3, 0.6, 0.3)  # Green button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 1.6)
        glVertex2f(2.0, 1.6)
        glVertex2f(2.0, 1.9)
        glVertex2f(1.0, 1.9)
        glEnd()
        draw_text("Against AI", 1.2, 1.75, (0, 0, 0))  # Black text

        # Close Button
        glColor3f(0.8, 0.3, 0.3)  # Red button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 1.0)
        glVertex2f(2.0, 1.0)
        glVertex2f(2.0, 1.3)
        glVertex2f(1.0, 1.3)
        glEnd()
        draw_text("Close", 1.3, 1.12, (0, 0, 0))  # Black text

    def draw_ai_choice(self):
        # Draw background
        glColor3f(0.15, 0.15, 0.2)  # Dark blue-gray background
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(3, 0)
        glVertex2f(3, 3)
        glVertex2f(0, 3)
        glEnd()

        # Title
        draw_text("Choose Your Color", 0.8, 2.6, (0.9, 0.9, 1.0))

        # Play as Blue Button
        glColor3f(0.2, 0.4, 1.0)  # Blue button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 2.0)
        glVertex2f(2.0, 2.0)
        glVertex2f(2.0, 2.3)
        glVertex2f(1.0, 2.3)
        glEnd()
        draw_text("Play as Blue", 1.1, 2.15, (0, 0, 0))

        # Play as Red Button
        glColor3f(1.0, 0.3, 0.3)  # Red button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 1.4)
        glVertex2f(2.0, 1.4)
        glVertex2f(2.0, 1.7)
        glVertex2f(1.0, 1.7)
        glEnd()
        draw_text("Play as Red", 1.2, 1.55, (0, 0, 0))

        # Exit Button
        glColor3f(0.8, 0.3, 0.3)  # Red button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 0.8)
        glVertex2f(2.0, 0.8)
        glVertex2f(2.0, 1.1)
        glVertex2f(1.0, 1.1)
        glEnd()
        draw_text("Exit", 1.3, 0.9, (0, 0, 0))

    def draw_win_screen(self):
        glColor3f(0.15, 0.15, 0.2)  
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(3, 0)
        glVertex2f(3, 3)
        glVertex2f(0, 3)
        glEnd()

        # Winner text
        if self.game.winning_player:
            text_color = (0.2, 0.4, 1.0) if self.game.winning_player == 'blue' else (1.0, 0.3, 0.3)
            message = f"{self.game.winning_player.capitalize()} Wins!"
        else:
            text_color = (0.9, 0.9, 1.0)
            message = "It's a Draw!"
        
        draw_text(message, 1.0, 2.2, text_color)

        # "Play Again" Button
        glColor3f(0.3, 0.6, 0.3)  # Green button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 1.5)
        glVertex2f(2.0, 1.5)
        glVertex2f(2.0, 1.8)
        glVertex2f(1.0, 1.8)
        glEnd()
        draw_text("Play Again", 1.15, 1.65, (0, 0, 0))

        # "Main Menu" Button
        glColor3f(0.2, 0.5, 0.8)  # Blue button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 1.0)
        glVertex2f(2.0, 1.0)
        glVertex2f(2.0, 1.3)
        glVertex2f(1.0, 1.3)
        glEnd()
        draw_text("Main Menu", 1.15, 1.15, (0, 0, 0))

        # "Close" Button
        glColor3f(0.8, 0.3, 0.3)  # Red button
        glBegin(GL_QUADS)
        glVertex2f(1.0, 0.5)
        glVertex2f(2.0, 0.5)
        glVertex2f(2.0, 0.8)
        glVertex2f(1.0, 0.8)
        glEnd()
        draw_text("Close", 1.3, 0.65, (0, 0, 0))