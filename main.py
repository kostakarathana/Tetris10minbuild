#!/usr/bin/env python3
"""
Tetris Game - Main Entry Point
A fully-featured Tetris implementation with cyberpunk theme
"""

import pygame
import sys
from tetris import TetrisGame

def main():
    """Initialize and run the Tetris game."""
    pygame.init()
    
    # Initialize the game
    game = TetrisGame()
    
    try:
        # Run the game
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()