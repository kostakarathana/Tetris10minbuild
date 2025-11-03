#!/bin/bash
# Tetris Game Launcher for Unix-like systems (Linux, macOS)

echo "🎮 Tetris - Cyberpunk Edition"
echo "=============================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is not available. Please install pip."
    exit 1
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements..."
    python3 -m pip install -r requirements.txt
fi

# Run the game
echo "🚀 Starting Tetris..."
python3 main.py