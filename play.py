#!/usr/bin/env python3
"""
Tetris Game Launcher
Simple launcher script with dependency checking
"""

import sys
import subprocess

def check_pygame():
    """Check if pygame is installed."""
    try:
        import pygame
        return True, pygame.version.ver
    except ImportError:
        return False, None

def install_pygame():
    """Install pygame using pip."""
    print("Installing pygame...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main launcher function."""
    print("🎮 Tetris - Cyberpunk Edition Launcher")
    print("=" * 50)
    
    # Check pygame
    has_pygame, version = check_pygame()
    
    if not has_pygame:
        print("❌ Pygame is not installed.")
        response = input("Would you like to install it automatically? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if install_pygame():
                print("✅ Pygame installed successfully!")
                has_pygame = True
            else:
                print("❌ Failed to install pygame. Please install it manually:")
                print("   pip install pygame")
                return 1
        else:
            print("Please install pygame manually and try again:")
            print("   pip install pygame")
            return 1
    else:
        print(f"✅ Pygame {version} is installed!")
    
    if has_pygame:
        print("\n🚀 Starting Tetris...")
        print("   Press SPACE or ENTER at the menu to start playing!")
        print("   Press ESC to quit the game anytime.")
        
        try:
            # Import and run the game
            from tetris import TetrisGame
            import pygame
            
            pygame.init()
            game = TetrisGame()
            game.run()
            
        except KeyboardInterrupt:
            print("\n👋 Game interrupted by user. Thanks for playing!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please check the error message above and try again.")
            return 1
        finally:
            try:
                pygame.quit()
            except:
                pass
    
    return 0

if __name__ == "__main__":
    sys.exit(main())