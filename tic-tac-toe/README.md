# Tic Tac Toe Game - Blue vs Red

This is a classic Tic Tac Toe game with a color twist, where players compete as either Blue or Red instead of X and O. The game is built using Python and OpenGL for graphics.

## Files Included

- main.py - The main game file that runs everything
- game.py - Handles all the game rules and logic
- renderer.py - Takes care of drawing the game on screen
- utils.py - Contains helper functions for the game

## How to Install

1. Make sure you have Python installed (version 3.6 or newer)
2. Install the required packages by running:
   pip install pyopengl glut

## How to Play

1. Run the game by executing:
   python main.py

2. When the game starts:
   - You'll see a main menu with options
   - Choose to play against a friend or against the computer
   - If playing against computer, pick your color (Blue or Red)

3. During the game:
   - Click on any empty square to place your mark
   - The game automatically checks for wins or ties
   - Blue always goes first
   - Press 'R' key anytime to reset the game

## Game Features

- Clean, colorful interface
- Smart computer opponent that's challenging to beat
- Animated winning line when someone wins
- Simple controls using just the mouse
- Clear menus and game screens

## Customizing the Game

You can change:
- The colors by editing values in renderer.py
- The window size in main.py
- The AI difficulty by modifying utils.py

## Known Issues

- The game window cannot be resized after starting
- Some systems may need additional OpenGL drivers

## Future Improvements Planned

- Adding different difficulty levels
- Including sound effects
- Making the window resizable
- Adding player score tracking

To report problems or suggest changes, please contact the developer.

Enjoy the game!