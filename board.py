"""
Tetris Game Board
Handles the game grid, collision detection, line clearing, and board state
"""

class TetrisBoard:
    """Manages the Tetris game board and its operations."""
    
    def __init__(self, width=10, height=20):
        """Initialize the game board."""
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
    def is_valid_position(self, piece):
        """Check if a piece can be placed at its current position."""
        blocks = piece.get_blocks()
        
        for x, y in blocks:
            # Check boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            # Check collision with existing blocks (but allow negative y for spawn area)
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def place_piece(self, piece):
        """Place a piece on the board permanently."""
        blocks = piece.get_blocks()
        
        for x, y in blocks:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.color
    
    def clear_lines(self):
        """Clear completed lines and return the number cleared."""
        lines_cleared = 0
        new_grid = []
        
        # Check each row from bottom to top
        for row in self.grid:
            if None in row:  # Row is not complete
                new_grid.append(row)
            else:  # Row is complete
                lines_cleared += 1
        
        # Add empty rows at the top
        while len(new_grid) < self.height:
            new_grid.insert(0, [None for _ in range(self.width)])
        
        self.grid = new_grid
        return lines_cleared
    
    def is_game_over(self):
        """Check if the game is over (blocks reached the top)."""
        # Check the top few rows for any blocks
        for row in range(min(4, self.height)):
            for col in range(self.width):
                if self.grid[row][col] is not None:
                    return True
        return False
    
    def get_ghost_piece(self, piece):
        """Get the ghost piece position (where the piece would land)."""
        ghost_piece = piece.copy()
        
        # Move the ghost piece down until it can't move anymore
        while self.is_valid_position(ghost_piece):
            ghost_piece.move(0, 1)
        
        # Move back one step to get the last valid position
        ghost_piece.move(0, -1)
        return ghost_piece
    
    def get_height_map(self):
        """Get the height of each column (for AI or difficulty calculation)."""
        heights = [0] * self.width
        
        for col in range(self.width):
            for row in range(self.height):
                if self.grid[row][col] is not None:
                    heights[col] = self.height - row
                    break
        
        return heights
    
    def get_holes_count(self):
        """Count the number of holes in the board."""
        holes = 0
        
        for col in range(self.width):
            block_found = False
            for row in range(self.height):
                if self.grid[row][col] is not None:
                    block_found = True
                elif block_found and self.grid[row][col] is None:
                    holes += 1
        
        return holes
    
    def clear(self):
        """Clear the entire board."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def copy(self):
        """Create a copy of the board."""
        new_board = TetrisBoard(self.width, self.height)
        new_board.grid = [row[:] for row in self.grid]
        return new_board