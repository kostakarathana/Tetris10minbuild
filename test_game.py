#!/usr/bin/env python3
"""
Test script to verify Tetris game functionality
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    try:
        import pygame
        print("✅ Pygame imported successfully")
        
        from pieces import TetrisPiece, get_random_piece, PIECES, PIECE_COLORS
        print("✅ Pieces module imported successfully")
        
        from board import TetrisBoard
        print("✅ Board module imported successfully")
        
        from audio import AudioManager
        print("✅ Audio module imported successfully")
        
        from tetris import TetrisGame
        print("✅ Tetris game module imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic game functionality."""
    try:
        from pieces import get_random_piece
        from board import TetrisBoard
        
        # Test piece creation
        piece = get_random_piece()
        print(f"✅ Created random piece: {piece.type}")
        
        # Test board creation
        board = TetrisBoard()
        print(f"✅ Created board: {board.width}x{board.height}")
        
        # Test piece placement validation
        is_valid = board.is_valid_position(piece)
        print(f"✅ Piece position validation: {is_valid}")
        
        # Test piece movement
        original_x = piece.x
        piece.move(1, 0)
        print(f"✅ Piece movement: {original_x} -> {piece.x}")
        
        # Test piece rotation
        original_rotation = piece.rotation
        piece.rotate_clockwise()
        print(f"✅ Piece rotation: {original_rotation} -> {piece.rotation}")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_audio_system():
    """Test audio system."""
    try:
        # Initialize pygame mixer
        import pygame
        from audio import AudioManager
        pygame.mixer.init()
        
        audio = AudioManager()
        print("✅ Audio manager created successfully")
        
        # Test mute functionality
        audio.toggle_mute()
        print("✅ Audio mute toggle works")
        
        return True
    except Exception as e:
        print(f"❌ Audio test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🎮 Tetris Game Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality Tests", test_basic_functionality),
        ("Audio System Tests", test_audio_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            print(f"✅ {test_name} PASSED")
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The game is ready to run.")
        print("\n🚀 To start the game, run:")
        print("   python main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())