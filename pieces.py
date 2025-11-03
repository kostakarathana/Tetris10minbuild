"""
Tetris Pieces (Tetrominoes) Definitions
Contains all 7 standard Tetris pieces with their rotations and properties
"""

import random

# Colors for each piece type (cyberpunk/neon theme)
PIECE_COLORS = {
    'I': (0, 255, 255),    # Cyan
    'O': (255, 255, 0),    # Yellow
    'T': (128, 0, 128),    # Purple
    'S': (0, 255, 0),      # Green
    'Z': (255, 0, 0),      # Red
    'J': (0, 0, 255),      # Blue
    'L': (255, 165, 0),    # Orange
}

# Piece shapes - each rotation is a 4x4 grid
PIECES = {
    'I': [
        [['....'],
         ['IIII'],
         ['....'],
         ['....']],
        
        [['..I.'],
         ['..I.'],
         ['..I.'],
         ['..I.']],
        
        [['....'],
         ['....'],
         ['IIII'],
         ['....']],
        
        [['.I..'],
         ['.I..'],
         ['.I..'],
         ['.I..']]
    ],
    
    'O': [
        [['....'],
         ['.OO.'],
         ['.OO.'],
         ['....']]
    ],
    
    'T': [
        [['....'],
         ['.T..'],
         ['TTT.'],
         ['....']],
        
        [['....'],
         ['.T..'],
         ['.TT.'],
         ['.T..']],
        
        [['....'],
         ['....'],
         ['TTT.'],
         ['.T..']],
        
        [['....'],
         ['.T..'],
         ['TT..'],
         ['.T..']]
    ],
    
    'S': [
        [['....'],
         ['.SS.'],
         ['SS..'],
         ['....']],
        
        [['....'],
         ['.S..'],
         ['.SS.'],
         ['..S.']]
    ],
    
    'Z': [
        [['....'],
         ['ZZ..'],
         ['.ZZ.'],
         ['....']],
        
        [['....'],
         ['..Z.'],
         ['.ZZ.'],
         ['.Z..']]
    ],
    
    'J': [
        [['....'],
         ['J...'],
         ['JJJ.'],
         ['....']],
        
        [['....'],
         ['.JJ.'],
         ['.J..'],
         ['.J..']],
        
        [['....'],
         ['....'],
         ['JJJ.'],
         ['..J.']],
        
        [['....'],
         ['.J..'],
         ['.J..'],
         ['JJ..']]
    ],
    
    'L': [
        [['....'],
         ['..L.'],
         ['LLL.'],
         ['....']],
        
        [['....'],
         ['.L..'],
         ['.L..'],
         ['.LL.']],
        
        [['....'],
         ['....'],
         ['LLL.'],
         ['L...']],
        
        [['....'],
         ['LL..'],
         ['.L..'],
         ['.L..']]
    ]
}

class TetrisPiece:
    """Represents a single Tetris piece with position and rotation."""
    
    def __init__(self, piece_type=None, x=0, y=0):
        """Initialize a Tetris piece."""
        if piece_type is None:
            piece_type = random.choice(list(PIECES.keys()))
        
        self.type = piece_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = PIECE_COLORS[piece_type]
        
    def get_shape(self):
        """Get the current shape matrix for this piece."""
        rotations = PIECES[self.type]
        return rotations[self.rotation % len(rotations)]
    
    def get_blocks(self):
        """Get the absolute positions of all blocks in this piece."""
        shape = self.get_shape()
        blocks = []
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row[0]):  # row is a list with one string
                if cell != '.':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        
        return blocks
    
    def rotate_clockwise(self):
        """Rotate the piece clockwise."""
        rotations = PIECES[self.type]
        self.rotation = (self.rotation + 1) % len(rotations)
    
    def rotate_counterclockwise(self):
        """Rotate the piece counterclockwise."""
        rotations = PIECES[self.type]
        self.rotation = (self.rotation - 1) % len(rotations)
    
    def move(self, dx, dy):
        """Move the piece by the given offset."""
        self.x += dx
        self.y += dy
    
    def copy(self):
        """Create a copy of this piece."""
        new_piece = TetrisPiece(self.type, self.x, self.y)
        new_piece.rotation = self.rotation
        return new_piece

def get_random_piece():
    """Get a random Tetris piece."""
    return TetrisPiece()

def get_piece_preview_shape(piece_type):
    """Get the shape for piece preview (first rotation)."""
    return PIECES[piece_type][0]