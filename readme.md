
# Tic Tac Toe with OpenGL

 Overview
A Python implementation of Tic Tac Toe featuring OpenGL graphics with two gameplay modes:
1. Local Multiplayer - Two players alternate turns on the same machine
2. AI Opponent - Play against an unbeatable minimax algorithm

 Technical Implementation

# Core Components
- Game Engine (`game.py`):
  - Manages 3x3 game board state
  - Tracks current player (X/O or Blue/Red)
  - Handles win/draw detection
  - Processes player moves

- Graphics System (`renderer.py`):
  - Renders game board using OpenGL primitives
  - Implements smooth win-line animation
  - Displays interactive menu system
  - Handles text rendering for UI elements

- AI Module (`utils.py`):
  - Minimax algorithm with alpha-beta pruning
  - Board evaluation function
  - Optimal move calculation

- Main Controller (`main.py`):
  - GLUT window management
  - Input handling (mouse/keyboard)
  - Game state transitions
  - Animation timing control

 Key Features

# Gameplay
- Turn-based grid placement
- Automatic win/draw detection
- Visual win indication (animated line)
- Configurable first player in AI mode

# Interface
- Responsive mouse controls
- Clean, minimalist design
- Immediate visual feedback
- Keyboard shortcut for reset (R key)

# AI Capabilities
- Perfect decision-making
- Immediate move calculation
- Adaptive difficulty (always plays optimally)

 Installation & Execution

# Requirements
- Python 3.6+
- PyOpenGL
- PyGLUT

bash
pip install PyOpenGL PyGLUT


# Launching the Game
bash
python src/main.py


 Architecture Diagram


Main Loop (main.py)
  ├── Game State (game.py)
  ├── Rendering Engine (renderer.py)
  └── AI Controller (utils.py)


 Development Notes

# Technical Considerations
- Fixed window size (600x600 pixels)
- Orthographic projection for 2D rendering
- Coordinate transformation for input handling
- Frame-independent animation timing

# Future Enhancements
- Difficulty levels for AI
- Score tracking
- Resizable window support
- Enhanced visual effects

 Maintenance

To report issues or contribute:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

This implementation provides a complete, production-ready Tic Tac Toe game with clean separation of concerns between game logic, rendering, and AI components.
