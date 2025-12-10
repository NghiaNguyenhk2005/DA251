"""player
Player character: movement, input handling, and sprite animation.

Notes:
- Uses Direction enum for clarity (avoid raw 0..3 integers).
- Reads all constants from the config namespace (cfg).
"""

import pygame
import os
import config as cfg
from enum import IntEnum


class Direction(IntEnum):
    """Movement directions as indices matching sprite layout mapping."""
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3

class Player:
    """Player character class with sprite-based walking animation"""
    
    def __init__(self, x, y):
        """
        Initialize the player
        
        Args:
            x, y: Starting position
        """
        self.x = x
        self.y = y
        self.speed = cfg.PLAYER_SPEED
        self.dx = 0
        self.dy = 0
        
        # Load sprite sheet
        sprite_path = os.path.join("src", "assets", "images", os.path.basename(cfg.SPRITE_SHEET_PATH))
        try:
            self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            self.use_sprites = True
            print(f"✅ Loaded sprite sheet: {sprite_path}")
        except Exception as e:
            self.sprite_sheet = None
            self.use_sprites = False
            print(f"⚠️  Could not load sprite sheet: {e}")
            print(f"   Using placeholder graphics instead")
        
        # Sprite dimensions from config
        self.sprite_width = cfg.SPRITE_WIDTH
        self.sprite_height = cfg.SPRITE_HEIGHT
        self.scale = cfg.SPRITE_SCALE
        
        # Calculate actual size after scaling
        self.width = self.sprite_width * self.scale
        self.height = self.sprite_height * self.scale
        
        # Create rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Direction mapping: 0=down, 1=right, 2=up, 3=left
        self.direction = Direction.DOWN
        self.direction_names = ['down', 'right', 'up', 'left']
        self.moving = False
        
        # Animation properties
        self.animation_frame = 0
        self.animation_speed = cfg.ANIMATION_SPEED
        self.idle_animation_speed = (
            cfg.IDLE_ANIMATION_SPEED if hasattr(cfg, "IDLE_ANIMATION_SPEED") else cfg.ANIMATION_SPEED * 0.5
        )
        self.animation_counter = 0
        
        # Load sprite layout from config
        self.sprite_layout = cfg.SPRITE_LAYOUT
        
        # Load all animation frames
        self.load_sprites()
        
        # Load idle frames
        self.load_idle_frames()
    
    def load_idle_frames(self):
        """Load idle animation frames for each direction"""
        self.idle_sprites = {
            0: [],  # Down
            1: [],  # Right
            2: [],  # Up
            3: []   # Left
        }
        
        if not self.use_sprites:
            return
        
        # Check if IDLE_LAYOUT is configured
        if not hasattr(cfg, "IDLE_LAYOUT") or cfg.IDLE_LAYOUT is None:
            # Use first frame of walking animation as idle
            print("🧍 Using first walking frame as idle pose")
            for direction_idx in range(4):
                if self.sprites[direction_idx]:
                    self.idle_sprites[direction_idx] = [self.sprites[direction_idx][0]]
            return
        
        print(f"\n🧍 Loading idle animation frames:")
        
        # Load idle animation frames for each direction
        for direction_idx, direction_name in enumerate(self.direction_names):
            if direction_name not in cfg.IDLE_LAYOUT:
                # Fallback to first walking frame
                if self.sprites[direction_idx]:
                    self.idle_sprites[direction_idx] = [self.sprites[direction_idx][0]]
                    print(f"   {direction_name.upper()}: Using first walk frame")
                continue
            
            row, frame_columns = cfg.IDLE_LAYOUT[direction_name]
            print(f"   {direction_name.upper()}: Row {row}, Frames {frame_columns}")
            
            for col in frame_columns:
                # Calculate position with spacing
                y_position = cfg.SPRITE_ROW_SPACING + (row * self.sprite_height) + (row * cfg.SPRITE_ROW_SPACING)
                x_position = (col * self.sprite_width) + (col * cfg.SPRITE_COL_SPACING)
                
                # Extract the idle sprite
                sprite_rect = pygame.Rect(
                    x_position,
                    y_position,
                    self.sprite_width,
                    self.sprite_height
                )
                
                # Create surface for idle frame
                sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
                sprite.blit(self.sprite_sheet, (0, 0), sprite_rect)
                
                # Scale up the sprite
                scaled_sprite = pygame.transform.scale(
                    sprite,
                    (self.width, self.height)
                )
                
                self.idle_sprites[direction_idx].append(scaled_sprite)
        
        total_idle_frames = sum(len(frames) for frames in self.idle_sprites.values())
        print(f"\n✅ Loaded {total_idle_frames} idle animation frames total")
    
    def load_sprites(self):
        """Load and process sprite frames from the sprite sheet using config"""
        self.sprites = {
            0: [],  # Down
            1: [],  # Right
            2: [],  # Up
            3: []   # Left
        }
        
        if not self.use_sprites:
            return
        
        print(f"\n📊 Sprite Configuration:")
        print(f"   Sprite size: {self.sprite_width}x{self.sprite_height} pixels")
        print(f"   Scale: {self.scale}x (final size: {self.width}x{self.height})")
        print(f"   Animation speed: {self.animation_speed}")
        print(f"\n🎬 Loading animation frames:")
        
        # Extract sprites for each direction using the config
        for direction_idx, direction_name in enumerate(self.direction_names):
            if direction_name not in self.sprite_layout:
                print(f"   ⚠️  Warning: '{direction_name}' not found in SPRITE_LAYOUT")
                continue
            
            row, frame_columns = self.sprite_layout[direction_name]
            print(f"   {direction_name.upper()}: Row {row}, Frames {frame_columns}")
            
            for col in frame_columns:
                # Calculate Y position with row spacing
                # Formula: y = initial_offset + (row * sprite_height) + (row * row_spacing)
                y_position = cfg.SPRITE_ROW_SPACING + (row * self.sprite_height) + (row * cfg.SPRITE_ROW_SPACING)
                
                # Calculate X position with column spacing (if any)
                x_position = (col * self.sprite_width) + (col * cfg.SPRITE_COL_SPACING)
                
                # Extract the sprite from the sheet
                sprite_rect = pygame.Rect(
                    x_position,                 # X position with column spacing
                    y_position,                 # Y position with row spacing
                    self.sprite_width,          # Width
                    self.sprite_height          # Height
                )
                
                # Debug: Print extraction coordinates for first frame
                if col == frame_columns[0]:
                    print(f"      → Extracting from: x={x_position}, y={y_position}, w={self.sprite_width}, h={self.sprite_height}")
                
                # Create a surface for this frame
                sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
                sprite.blit(self.sprite_sheet, (0, 0), sprite_rect)
                
                # Scale up the sprite
                scaled_sprite = pygame.transform.scale(
                    sprite,
                    (self.width, self.height)
                )
                
                self.sprites[direction_idx].append(scaled_sprite)
        
        print(f"\n✅ Loaded {sum(len(frames) for frames in self.sprites.values())} sprite frames total\n")
    
    def handle_input(self, keys):
        """
        Handle keyboard input for movement intent.
        Sets dx and dy velocity components based on key presses.
        """
        self.dx = 0
        self.dy = 0

        # Check for movement keys and set velocity
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.dx += 1
    
    def update(self):
        """
        Update player state: move the player based on velocity,
        update rect, handle animations, and set direction.
        """
        self.moving = self.dx != 0 or self.dy != 0

        # Apply movement
        if self.moving:
            move_speed = self.speed
            # Normalize for diagonal movement
            if self.dx != 0 and self.dy != 0:
                move_speed *= 0.7071  # approx. 1 / sqrt(2)
            
            self.x += self.dx * move_speed
            self.y += self.dy * move_speed

            # Update direction based on which key was likely pressed last.
            # This is a simple priority: vertical keys take precedence.
            if self.dy < 0:
                self.direction = Direction.UP
            elif self.dy > 0:
                self.direction = Direction.DOWN
            elif self.dx < 0:
                self.direction = Direction.LEFT
            elif self.dx > 0:
                self.direction = Direction.RIGHT

        # Keep player within screen bounds
        self.x = max(0, min(self.x, cfg.SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, cfg.SCREEN_HEIGHT - self.height))

        # IMPORTANT: Update rect to reflect new position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Update animation frame
        current_animation_speed = self.animation_speed if self.moving else self.idle_animation_speed
        self.animation_counter += current_animation_speed
        
        if self.animation_counter >= 1:
            self.animation_counter = 0
            
            # Choose correct set of frames (walking or idle)
            animation_frames = self.sprites[self.direction.value] if self.moving else self.idle_sprites[self.direction.value]
            num_frames = len(animation_frames)
            
            if num_frames > 0:
                self.animation_frame = (self.animation_frame + 1) % num_frames
    
    def draw(self, screen):
        """
        Draw the player on the screen with sprite animation
        
        Args:
            screen: Pygame surface to draw on
        """
        # Calculate center position (used for fallback and footsteps)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if self.use_sprites:
            # Choose sprite: idle or walking animation
            current_sprite = None
            
            if not self.moving and self.idle_sprites[self.direction.value]:
                # Use idle sprite animation when standing still
                idle_frames = self.idle_sprites[self.direction.value]
                if idle_frames and len(idle_frames) > 0:
                    # Make sure frame index is within bounds
                    frame_idx = self.animation_frame % len(idle_frames)
                    current_sprite = idle_frames[frame_idx]
            elif self.sprites[self.direction.value]:
                # Use walking animation when moving
                walk_frames = self.sprites[self.direction.value]
                if walk_frames and len(walk_frames) > 0:
                    # Make sure frame index is within bounds
                    frame_idx = self.animation_frame % len(walk_frames)
                    current_sprite = walk_frames[frame_idx]
            
            if current_sprite:
                screen.blit(current_sprite, (self.x, self.y))
            else:
                # Fallback if sprite is None
                pygame.draw.rect(screen, cfg.BLUE, self.rect)
        else:
            # Fallback: Draw simple colored rectangle if sprites not loaded
            pygame.draw.rect(screen, cfg.BLUE, self.rect)
            
            # Draw direction indicator
            if self.direction == Direction.DOWN:
                points = [(center_x, self.y + self.height), (center_x - 5, center_y), (center_x + 5, center_y)]
            elif self.direction == Direction.RIGHT:
                points = [(self.x + self.width, center_y), (center_x, center_y - 5), (center_x, center_y + 5)]
            elif self.direction == Direction.UP:
                points = [(center_x, self.y), (center_x - 5, center_y), (center_x + 5, center_y)]
            else:  # Left
                points = [(self.x, center_y), (center_x, center_y - 5), (center_x, center_y + 5)]
            
            pygame.draw.polygon(screen, cfg.YELLOW, points)
        
        # Draw animated footsteps (dots that appear when moving)
        if self.moving and self.animation_frame in [1, 3]:
            foot_offset = 6
            if self.direction in (Direction.DOWN, Direction.UP):
                pygame.draw.circle(screen, cfg.WHITE, (int(center_x - foot_offset), int(self.y + self.height)), 2)
                pygame.draw.circle(screen, cfg.WHITE, (int(center_x + foot_offset), int(self.y + self.height)), 2)
            else:  # Left/Right
                pygame.draw.circle(screen, cfg.WHITE, (int(center_x), int(center_y - foot_offset)), 2)
                pygame.draw.circle(screen, cfg.WHITE, (int(center_x), int(center_y + foot_offset)), 2)
