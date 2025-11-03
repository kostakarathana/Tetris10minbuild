"""
Audio Manager for Tetris
Handles sound effects and background music
"""

import pygame
import os

class AudioManager:
    """Manages game audio including sound effects and music."""
    
    def __init__(self):
        """Initialize the audio system."""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.muted = False
        
        # Try to load sounds if they exist
        self.load_sounds()
        
    def load_sounds(self):
        """Load sound effects. Creates placeholder sounds if files don't exist."""
        sound_files = {
            'move': None,
            'rotate': None,
            'drop': None,
            'line_clear': None,
            'tetris': None,
            'game_over': None,
            'level_up': None
        }
        
        # For now, we'll create simple programmatic sounds
        # In a full implementation, you'd load actual sound files
        self.create_simple_sounds()
        
    def create_simple_sounds(self):
        """Create simple programmatic sound effects."""
        try:
            # Create simple beep sounds using pygame
            # Move sound - short low beep
            self.sounds['move'] = self.create_tone(220, 0.1)
            
            # Rotate sound - quick chirp
            self.sounds['rotate'] = self.create_tone(440, 0.08)
            
            # Drop sound - descending tone
            self.sounds['drop'] = self.create_sweep_tone(440, 220, 0.2)
            
            # Line clear - ascending arpeggio
            self.sounds['line_clear'] = self.create_arpeggio([261, 329, 392, 523], 0.15)
            
            # Tetris (4 lines) - victory fanfare
            self.sounds['tetris'] = self.create_arpeggio([261, 329, 392, 523, 659], 0.3)
            
            # Game over - descending sad tone
            self.sounds['game_over'] = self.create_sweep_tone(523, 130, 1.0)
            
            # Level up - triumphant beep
            self.sounds['level_up'] = self.create_arpeggio([392, 523, 659, 784], 0.2)
            
        except Exception as e:
            print(f"Could not create sounds: {e}")
            # Disable sounds if creation fails
            self.sounds = {}
    
    def create_tone(self, frequency, duration, sample_rate=22050):
        """Create a simple tone sound."""
        import numpy as np
        
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            # Apply envelope to avoid clicks
            envelope = min(1.0, i / (sample_rate * 0.01), (frames - i) / (sample_rate * 0.01))
            arr[i][0] = wave * envelope * 0.3  # Left channel
            arr[i][1] = wave * envelope * 0.3  # Right channel
        
        # Convert to pygame sound
        sound_array = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(sound_array)
        return sound
    
    def create_sweep_tone(self, start_freq, end_freq, duration, sample_rate=22050):
        """Create a frequency sweep tone."""
        try:
            import numpy as np
            
            frames = int(duration * sample_rate)
            arr = np.zeros((frames, 2))
            
            for i in range(frames):
                # Linear frequency interpolation
                progress = i / frames
                current_freq = start_freq + (end_freq - start_freq) * progress
                
                wave = np.sin(2 * np.pi * current_freq * i / sample_rate)
                # Apply envelope
                envelope = min(1.0, i / (sample_rate * 0.01), (frames - i) / (sample_rate * 0.01))
                arr[i][0] = wave * envelope * 0.3
                arr[i][1] = wave * envelope * 0.3
            
            sound_array = (arr * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback if numpy not available
            return self.create_tone(start_freq, duration)
    
    def create_arpeggio(self, frequencies, total_duration, sample_rate=22050):
        """Create an arpeggio from a list of frequencies."""
        try:
            import numpy as np
            
            note_duration = total_duration / len(frequencies)
            frames_per_note = int(note_duration * sample_rate)
            total_frames = frames_per_note * len(frequencies)
            
            arr = np.zeros((total_frames, 2))
            
            for note_idx, freq in enumerate(frequencies):
                start_frame = note_idx * frames_per_note
                for i in range(frames_per_note):
                    frame_idx = start_frame + i
                    if frame_idx < total_frames:
                        wave = np.sin(2 * np.pi * freq * i / sample_rate)
                        # Apply envelope to each note
                        note_progress = i / frames_per_note
                        envelope = min(1.0, 
                                     note_progress / 0.1,  # Attack
                                     (1 - note_progress) / 0.1)  # Release
                        arr[frame_idx][0] = wave * envelope * 0.3
                        arr[frame_idx][1] = wave * envelope * 0.3
            
            sound_array = (arr * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound
        except ImportError:
            # Fallback if numpy not available
            return self.create_tone(frequencies[0], total_duration)
    
    def play_sound(self, sound_name):
        """Play a sound effect."""
        if not self.muted and sound_name in self.sounds and self.sounds[sound_name]:
            try:
                sound = self.sounds[sound_name]
                sound.set_volume(self.sfx_volume)
                sound.play()
            except Exception as e:
                print(f"Could not play sound {sound_name}: {e}")
    
    def play_move_sound(self):
        """Play piece move sound."""
        self.play_sound('move')
    
    def play_rotate_sound(self):
        """Play piece rotation sound."""
        self.play_sound('rotate')
    
    def play_drop_sound(self):
        """Play piece drop sound."""
        self.play_sound('drop')
    
    def play_line_clear_sound(self, lines_cleared):
        """Play line clear sound based on number of lines."""
        if lines_cleared == 4:
            self.play_sound('tetris')
        elif lines_cleared > 0:
            self.play_sound('line_clear')
    
    def play_game_over_sound(self):
        """Play game over sound."""
        self.play_sound('game_over')
    
    def play_level_up_sound(self):
        """Play level up sound."""
        self.play_sound('level_up')
    
    def toggle_mute(self):
        """Toggle mute state."""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if not self.muted:
            pygame.mixer.music.set_volume(self.music_volume)