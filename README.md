# Tetris - Cyberpunk Edition 🎮

A fully-featured Tetris game built with Python and Pygame, featuring a sleek cyberpunk theme, complete with all standard Tetris mechanics and immersive sound effects.

## Features ✨

### Core Tetris Features
- ✅ All 7 standard Tetromino pieces (I, O, T, S, Z, J, L)
- ✅ Piece rotation with wall kick system
- ✅ Line clearing with proper scoring
- ✅ Progressive difficulty (speed increases with level)
- ✅ Ghost piece preview (shows where piece will land)
- ✅ Hold functionality
- ✅ Next piece preview
- ✅ Soft drop and hard drop

### Visual Features
- 🎨 Cyberpunk/Neon theme with vibrant colors
- 🔮 Glowing grid lines and piece borders
- 👻 Semi-transparent ghost piece
- 🎯 Clean, modern UI with score, level, and lines display
- 📱 Responsive controls display

### Audio Features
- 🔊 Procedurally generated sound effects
- 🎵 Different sounds for movement, rotation, drops, line clears
- 🏆 Special sound for Tetris (4-line clear)
- 📢 Level up and game over sounds
- 🔇 Mute toggle functionality

### Game States
- 🏠 Main menu
- ⏸️ Pause functionality
- 💀 Game over screen with restart options
- 🎮 Smooth state transitions

## Installation & Requirements 📦

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Required Packages
```bash
pip install pygame
```

For enhanced audio features (optional):
```bash
pip install numpy
```

### Quick Setup

**Option 1: Simple (Recommended)**
```bash
cd Tetris10minbuild
python main.py
```

**Option 2: With automatic dependency installation**
```bash
cd Tetris10minbuild  
python play.py
```

**Option 3: Using requirements file**
```bash
cd Tetris10minbuild
pip install -r requirements.txt
python main.py
```

**Option 4: Unix/Linux/macOS shell script**
```bash
cd Tetris10minbuild
./run.sh
```

## How to Play 🎯

### Controls
| Key | Action |
|-----|--------|
| ←→ | Move piece left/right |
| ↓ | Soft drop (faster fall) |
| ↑ or Z | Rotate piece clockwise |
| X | Rotate piece counterclockwise |
| Space | Hard drop (instant drop) |
| C | Hold current piece |
| M | Toggle mute |
| P or Esc | Pause game |

### Scoring System
- **Single line**: 40 × level
- **Double lines**: 100 × level  
- **Triple lines**: 300 × level
- **Tetris (4 lines)**: 1200 × level
- **Hard drop**: 2 points per cell dropped

### Level Progression
- Level increases every 10 lines cleared
- Fall speed increases with each level
- Maximum level: 15

## Game Features Deep Dive 🔍

### Piece System
- **7 Standard Pieces**: All classic Tetromino shapes with proper rotations
- **Wall Kicks**: Advanced rotation system allows pieces to "kick" off walls
- **Ghost Piece**: Shows exactly where your piece will land
- **Hold Queue**: Save a piece for later use (once per piece)
- **Next Piece**: Preview the next piece to plan ahead

### Visual Design
- **Cyberpunk Theme**: Neon colors (cyan, green, pink, purple) on dark background
- **Glowing Effects**: Subtle alpha blending for visual depth
- **Clean Grid**: Professional-looking game board with clear boundaries
- **Modern UI**: Score, level, and control information clearly displayed

### Audio System
- **Procedural Sounds**: No external sound files needed
- **Dynamic Audio**: Different sounds for different actions
- **Volume Control**: Built-in mute functionality
- **Immersive Effects**: Audio feedback enhances gameplay experience

## File Structure 📁

```
Tetris10minbuild/
├── main.py          # Game entry point - run this to play!
├── tetris.py        # Main game logic and rendering
├── pieces.py        # Tetromino definitions and piece logic  
├── board.py         # Game board and collision detection
├── audio.py         # Sound effects and audio management
├── play.py          # Alternative launcher with dependency checking
├── test_game.py     # Test suite to verify game functionality
├── run.sh           # Shell script launcher (Unix/Linux/macOS)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Technical Implementation 🛠️

### Architecture
- **Modular Design**: Separate files for different game systems
- **Clean Interfaces**: Well-defined classes and methods
- **Extensible Code**: Easy to add new features or modify existing ones

### Performance
- **60 FPS**: Smooth gameplay with consistent frame rate
- **Efficient Rendering**: Optimized drawing calls
- **Memory Management**: Proper cleanup and resource management

### Compatibility
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Pure Python**: No external dependencies except Pygame
- **Minimal Requirements**: Low system requirements

## Customization 🎨

Want to modify the game? Here are some easy customization points:

### Colors
Edit the color constants in `tetris.py`:
```python
NEON_BLUE = (0, 255, 255)
NEON_GREEN = (0, 255, 0)
NEON_PINK = (255, 0, 255)
# ... etc
```

### Game Speed
Modify the fall speed calculation in `tetris.py`:
```python
def update_fall_speed(self):
    self.fall_speed = max(50, 500 - (self.level - 1) * 50)
```

### Board Size
Change the board dimensions in `tetris.py`:
```python
BOARD_WIDTH = 10    # Standard is 10
BOARD_HEIGHT = 20   # Standard is 20
```

### Scoring
Adjust the scoring system in the `calculate_score` method.

## Troubleshooting 🔧

### Common Issues

**"No module named 'pygame'"**
```bash
pip install pygame
```

**Audio not working**
- Install numpy for enhanced audio: `pip install numpy`
- Check if your system supports pygame audio
- Try running with `M` key to toggle mute/unmute

**Game running too slow/fast**
- The game targets 60 FPS but will adapt to your system
- Close other applications to free up resources

**Controls not responsive**
- Make sure the game window has focus
- Try running in fullscreen or windowed mode

## Contributing 🤝

Want to improve the game? Here are some ideas:
- Add more visual effects (particles, animations)
- Implement different game modes (Sprint, Ultra, etc.)
- Add multiplayer support
- Create custom themes
- Add high score system with persistence
- Implement T-spin detection and bonuses

## License 📄

This project is open source and available for educational and personal use.

## Credits 🙏

- **Game Design**: Based on the classic Tetris by Alexey Pajitnov
- **Implementation**: Built with Python and Pygame
- **Audio**: Procedural sound generation
- **Theme**: Cyberpunk/neon aesthetic inspired by retro-futurism

---

**Enjoy the game! 🎮✨**

*Press any key to start your Tetris journey...*