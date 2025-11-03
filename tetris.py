"""
Main Tetris Game Logic
Handles game mechanics, input, rendering, and game state management
"""

import pygame
import random
import math
from board import TetrisBoard
from pieces import TetrisPiece, get_random_piece, PIECE_COLORS
from audio import AudioManager

# Game constants
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
BOARD_X_OFFSET = 100
BOARD_Y_OFFSET = 50

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Colors (Cyberpunk/Neon theme)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
NEON_BLUE = (0, 255, 255)
NEON_GREEN = (0, 255, 0)
NEON_PINK = (255, 0, 255)
NEON_PURPLE = (128, 0, 255)
GRID_COLOR = (32, 32, 64)

# Game states
GAME_STATE_MENU = 'menu'
GAME_STATE_PLAYING = 'playing'
GAME_STATE_PAUSED = 'paused'
GAME_STATE_GAME_OVER = 'game_over'

class TetrisGame:
    """Main Tetris game class."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize Pygame
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Cyberpunk Edition")
        
        # Initialize clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Initialize audio
        self.audio = AudioManager()
        
        # Game state
        self.state = GAME_STATE_MENU
        self.running = True
        
        # Initialize game components
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = TetrisBoard(BOARD_WIDTH, BOARD_HEIGHT)
        self.current_piece = get_random_piece()
        self.current_piece.x = BOARD_WIDTH // 2 - 2
        self.current_piece.y = 0
        
        self.next_piece = get_random_piece()
        self.hold_piece = None
        self.can_hold = True
        
        # Game statistics
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        
        # Timing
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.last_time = pygame.time.get_ticks()
        
        # Visual effects
        self.line_clear_animation = 0
        self.cleared_lines = []
        
    def update_fall_speed(self):
        """Update fall speed based on level."""
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
    def calculate_score(self, lines_cleared):
        """Calculate score based on lines cleared."""
        base_scores = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        return base_scores.get(lines_cleared, 0) * self.level
        
    def handle_input(self):
        """Handle keyboard input."""
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # Handle continuous key presses
        if hasattr(self, 'key_timers'):
            for key, timer in self.key_timers.items():
                if keys[key] and current_time - timer > 100:  # 100ms repeat rate
                    if key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                    self.key_timers[key] = current_time
        else:
            self.key_timers = {}
            
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if self.state == GAME_STATE_MENU:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = GAME_STATE_PLAYING
                        
                elif self.state == GAME_STATE_PLAYING:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                        self.key_timers[pygame.K_LEFT] = current_time
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                        self.key_timers[pygame.K_RIGHT] = current_time
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                        self.key_timers[pygame.K_DOWN] = current_time
                    elif event.key == pygame.K_UP or event.key == pygame.K_z:
                        self.rotate_piece()
                    elif event.key == pygame.K_x:
                        self.rotate_piece(clockwise=False)
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                    elif event.key == pygame.K_c:
                        self.hold_current_piece()
                    elif event.key == pygame.K_m:
                        self.audio.toggle_mute()
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = GAME_STATE_PAUSED
                        
                elif self.state == GAME_STATE_PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = GAME_STATE_PLAYING
                        
                elif self.state == GAME_STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = GAME_STATE_PLAYING
                    elif event.key == pygame.K_m:
                        self.state = GAME_STATE_MENU
                        
            elif event.type == pygame.KEYUP:
                if event.key in self.key_timers:
                    del self.key_timers[event.key]
                    
    def move_piece(self, dx, dy):
        """Move the current piece."""
        if self.state != GAME_STATE_PLAYING:
            return False
            
        original_x, original_y = self.current_piece.x, self.current_piece.y
        self.current_piece.move(dx, dy)
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x, self.current_piece.y = original_x, original_y
            return False
        
        # Play move sound if piece moved successfully
        if dx != 0 or dy != 0:
            self.audio.play_move_sound()
        return True
        
    def rotate_piece(self, clockwise=True):
        """Rotate the current piece with wall kicks."""
        if self.state != GAME_STATE_PLAYING:
            return
            
        original_rotation = self.current_piece.rotation
        
        # Try basic rotation
        if clockwise:
            self.current_piece.rotate_clockwise()
        else:
            self.current_piece.rotate_counterclockwise()
            
        # If rotation is invalid, try wall kicks
        if not self.board.is_valid_position(self.current_piece):
            wall_kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
            
            kicked = False
            for dx, dy in wall_kicks:
                self.current_piece.move(dx, dy)
                if self.board.is_valid_position(self.current_piece):
                    kicked = True
                    self.audio.play_rotate_sound()
                    break
                self.current_piece.move(-dx, -dy)
                
            if not kicked:
                # Revert rotation
                self.current_piece.rotation = original_rotation
        else:
            # Basic rotation succeeded
            self.audio.play_rotate_sound()
                
    def hard_drop(self):
        """Drop the piece to the bottom."""
        if self.state != GAME_STATE_PLAYING:
            return
            
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1
            
        # Add score for hard drop
        self.score += drop_distance * 2
        
        # Play drop sound
        self.audio.play_drop_sound()
        
        # Place the piece immediately
        self.place_current_piece()
        
    def hold_current_piece(self):
        """Hold/swap the current piece."""
        if not self.can_hold or self.state != GAME_STATE_PLAYING:
            return
            
        if self.hold_piece is None:
            self.hold_piece = TetrisPiece(self.current_piece.type)
            self.spawn_next_piece()
        else:
            # Swap pieces
            temp_type = self.hold_piece.type
            self.hold_piece = TetrisPiece(self.current_piece.type)
            self.current_piece = TetrisPiece(temp_type)
            self.current_piece.x = BOARD_WIDTH // 2 - 2
            self.current_piece.y = 0
            
        self.can_hold = False
        
    def spawn_next_piece(self):
        """Spawn the next piece."""
        self.current_piece = self.next_piece
        self.current_piece.x = BOARD_WIDTH // 2 - 2
        self.current_piece.y = 0
        self.next_piece = get_random_piece()
        self.can_hold = True
        
        # Check game over
        if not self.board.is_valid_position(self.current_piece):
            self.state = GAME_STATE_GAME_OVER
            self.audio.play_game_over_sound()
            
    def place_current_piece(self):
        """Place the current piece on the board."""
        self.board.place_piece(self.current_piece)
        
        # Check for line clears
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            old_level = self.level
            self.lines_cleared += lines_cleared
            self.score += self.calculate_score(lines_cleared)
            self.level = min(15, 1 + self.lines_cleared // 10)
            self.update_fall_speed()
            
            # Play appropriate sound
            self.audio.play_line_clear_sound(lines_cleared)
            
            # Play level up sound if level increased
            if self.level > old_level:
                self.audio.play_level_up_sound()
            
        self.spawn_next_piece()
        
    def update(self):
        """Update game logic."""
        if self.state != GAME_STATE_PLAYING:
            return
            
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Handle falling
        self.fall_time += delta_time
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_current_piece()
            self.fall_time = 0
            
    def draw_grid(self):
        """Draw the game grid."""
        # Draw board background
        board_rect = pygame.Rect(
            BOARD_X_OFFSET - 2, BOARD_Y_OFFSET - 2,
            BOARD_WIDTH * CELL_SIZE + 4, BOARD_HEIGHT * CELL_SIZE + 4
        )
        pygame.draw.rect(self.screen, NEON_BLUE, board_rect, 2)
        
        # Draw grid lines
        for x in range(BOARD_WIDTH + 1):
            start_x = BOARD_X_OFFSET + x * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                           (start_x, BOARD_Y_OFFSET),
                           (start_x, BOARD_Y_OFFSET + BOARD_HEIGHT * CELL_SIZE))
        
        for y in range(BOARD_HEIGHT + 1):
            start_y = BOARD_Y_OFFSET + y * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR,
                           (BOARD_X_OFFSET, start_y),
                           (BOARD_X_OFFSET + BOARD_WIDTH * CELL_SIZE, start_y))
                           
    def draw_piece(self, piece, alpha=255):
        """Draw a piece on the board."""
        if piece is None:
            return
            
        blocks = piece.get_blocks()
        
        for x, y in blocks:
            if 0 <= x < BOARD_WIDTH and y >= 0:
                screen_x = BOARD_X_OFFSET + x * CELL_SIZE
                screen_y = BOARD_Y_OFFSET + y * CELL_SIZE
                
                if screen_y < BOARD_Y_OFFSET + BOARD_HEIGHT * CELL_SIZE:
                    # Create surface for alpha blending
                    block_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    block_surface.fill(piece.color)
                    block_surface.set_alpha(alpha)
                    
                    # Draw block
                    self.screen.blit(block_surface, (screen_x, screen_y))
                    
                    # Draw border
                    pygame.draw.rect(self.screen, WHITE,
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)
                                   
    def draw_board_blocks(self):
        """Draw the placed blocks on the board."""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board.grid[y][x] is not None:
                    screen_x = BOARD_X_OFFSET + x * CELL_SIZE
                    screen_y = BOARD_Y_OFFSET + y * CELL_SIZE
                    
                    # Draw block
                    pygame.draw.rect(self.screen, self.board.grid[y][x],
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                    
                    # Draw border
                    pygame.draw.rect(self.screen, WHITE,
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)
                                   
    def draw_ghost_piece(self):
        """Draw the ghost piece (projection)."""
        ghost_piece = self.board.get_ghost_piece(self.current_piece)
        self.draw_piece(ghost_piece, alpha=64)
        
    def draw_ui(self):
        """Draw the user interface."""
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, NEON_GREEN)
        self.screen.blit(score_text, (450, 100))
        
        # Lines
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, NEON_GREEN)
        self.screen.blit(lines_text, (450, 140))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, NEON_GREEN)
        self.screen.blit(level_text, (450, 180))
        
        # Next piece
        next_text = self.font_medium.render("Next:", True, NEON_PINK)
        self.screen.blit(next_text, (450, 240))
        
        # Draw next piece preview
        if self.next_piece:
            preview_x, preview_y = 470, 270
            blocks = self.next_piece.get_blocks()
            for x, y in blocks:
                screen_x = preview_x + x * 20
                screen_y = preview_y + y * 20
                pygame.draw.rect(self.screen, self.next_piece.color,
                               (screen_x, screen_y, 20, 20))
                pygame.draw.rect(self.screen, WHITE,
                               (screen_x, screen_y, 20, 20), 1)
        
        # Hold piece
        if self.hold_piece:
            hold_text = self.font_medium.render("Hold:", True, NEON_PINK)
            self.screen.blit(hold_text, (450, 370))
            
            preview_x, preview_y = 470, 400
            blocks = self.hold_piece.get_blocks()
            for x, y in blocks:
                screen_x = preview_x + x * 20
                screen_y = preview_y + y * 20
                pygame.draw.rect(self.screen, self.hold_piece.color,
                               (screen_x, screen_y, 20, 20))
                pygame.draw.rect(self.screen, WHITE,
                               (screen_x, screen_y, 20, 20), 1)
        
        # Controls
        controls = [
            "Controls:",
            "←→ Move",
            "↓ Soft Drop",
            "↑/Z Rotate",
            "Space Hard Drop",
            "C Hold",
            "M Mute",
            "P Pause"
        ]
        
        for i, control in enumerate(controls):
            color = NEON_PURPLE if i == 0 else WHITE
            control_text = self.font_small.render(control, True, color)
            self.screen.blit(control_text, (450, 500 + i * 25))
            
    def draw_menu(self):
        """Draw the main menu."""
        title_text = self.font_large.render("TETRIS", True, NEON_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_medium.render("Cyberpunk Edition", True, NEON_PINK)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        start_text = self.font_medium.render("Press SPACE or ENTER to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(start_text, start_rect)
        
    def draw_pause_screen(self):
        """Draw the pause screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("PAUSED", True, NEON_BLUE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_medium.render("Press P or ESC to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
        
    def draw_game_over_screen(self):
        """Draw the game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(192)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, NEON_PINK)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, NEON_GREEN)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        restart_text = self.font_medium.render("Press R to restart or M for menu", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
    def draw(self):
        """Draw everything."""
        self.screen.fill(BLACK)
        
        if self.state == GAME_STATE_MENU:
            self.draw_menu()
        else:
            # Draw game elements
            self.draw_grid()
            self.draw_board_blocks()
            
            if self.state == GAME_STATE_PLAYING:
                self.draw_ghost_piece()
                self.draw_piece(self.current_piece)
            
            self.draw_ui()
            
            if self.state == GAME_STATE_PAUSED:
                self.draw_pause_screen()
            elif self.state == GAME_STATE_GAME_OVER:
                self.draw_game_over_screen()
        
        pygame.display.flip()
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS