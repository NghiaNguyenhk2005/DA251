"""config
Centralized game configuration constants.

Organized sections:
    - Screen / window
    - Color palette
    - Player & animation settings
    - Sprite sheet layout configuration
    - Game meta / limits
    - Rendering helpers (grid + instructional overlay)

Only place project‑wide magic numbers should live. Keep runtime mutable
settings (e.g., volume, keybinds) elsewhere later.
"""

# ---------------------------------------------------------------------------
# Screen / Window settings
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Se7en Detective"

# ---------------------------------------------------------------------------
# Color palette (RGB)
# ---------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# ---------------------------------------------------------------------------
# Player settings
# ---------------------------------------------------------------------------
PLAYER_SPEED = 5
PLAYER_SIZE = 32

# ---------------------------------------------------------------------------
# Sprite settings
# ---------------------------------------------------------------------------
SPRITE_SHEET_PATH = "assets/images/Modern_Exteriors_Characters_Postman_16x16_2.png"
SPRITE_WIDTH = 16          # Width of each sprite in the sheet (in pixels)
SPRITE_HEIGHT = 24         # Height of each sprite in the sheet (in pixels)
SPRITE_SCALE = 8           # How much to scale up the sprite (2 = double size)
SPRITE_ROW_SPACING = 8     # Vertical spacing between rows in pixels
SPRITE_COL_SPACING = 0     # Horizontal spacing between columns in pixels

# Sprite sheet layout configuration
# Format: direction_name: (row_in_sheet, [list of column numbers for animation frames])
# 
# HOW TO CUSTOMIZE FRAMES:
# Simply add or remove column numbers from the list!
# Example: [0, 1, 2, 3, 4, 5] uses 6 frames
# Example: [1, 2] uses only 2 frames
# Example: [0, 1, 2, 3, 2, 1] creates a "ping-pong" animation (goes back and forth)

SPRITE_LAYOUT = {
    "right": (2, [0, 1, 2, 3, 4, 5]),
    "up":    (2, [6, 7, 8, 9, 10, 11]),
    "left":  (2, [12, 13, 14, 15, 16, 17]),
    "down":  (2, [18, 19, 20, 21, 22, 23]),
}

# Idle animation configuration
# Format: direction_name: (row, [columns]) - frames to use when standing still
# This allows each direction to have its own idle animation!
IDLE_LAYOUT = {
    "right": (1, [0, 1, 2, 3, 4, 5]),
    "up":    (1, [6, 7, 8, 9, 10, 11]),
    "left":  (1, [12, 13, 14, 15, 16, 17]),
    "down":  (1, [18, 19, 20, 21, 22, 23]),
}

# Idle animation speed (usually slower than walking)
IDLE_ANIMATION_SPEED = 0.08   # Slower breathing/idle animation

# Alternative: Set to None to use first frame of walking animation
# IDLE_LAYOUT = None

# ═══════════════════════════════════════════════════════════════════════════
# 📚 MORE FRAME EXAMPLES - Uncomment to use!
# ═══════════════════════════════════════════════════════════════════════════

# Example 1: Use 6 frames for smoother animation
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 1, 2, 3, 4, 5]),
#     'right': (1, [0, 1, 2, 3, 4, 5]),
#     'up':    (2, [0, 1, 2, 3, 4, 5]),
#     'left':  (3, [0, 1, 2, 3, 4, 5])
# }

# Example 2: Use 8 frames (full row)
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 1, 2, 3, 4, 5, 6, 7]),
#     'right': (1, [0, 1, 2, 3, 4, 5, 6, 7]),
#     'up':    (2, [0, 1, 2, 3, 4, 5, 6, 7]),
#     'left':  (3, [0, 1, 2, 3, 4, 5, 6, 7])
# }

# Example 3: Different number of frames per direction
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 1, 2, 3, 4, 5]),     # 6 frames for down
#     'right': (1, [0, 1, 2, 3]),           # 4 frames for right
#     'up':    (2, [0, 1, 2, 3, 4, 5]),     # 6 frames for up
#     'left':  (3, [0, 1, 2, 3])            # 4 frames for left
# }

# Example 4: Skip the first frame (idle pose)
# SPRITE_LAYOUT = {
#     'down':  (0, [1, 2, 3, 4]),
#     'right': (1, [1, 2, 3, 4]),
#     'up':    (2, [1, 2, 3, 4]),
#     'left':  (3, [1, 2, 3, 4])
# }

# Example 5: Ping-pong animation (smooth back-and-forth)
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 1, 2, 3, 2, 1]),     # Goes 0→1→2→3→2→1→repeat
#     'right': (1, [0, 1, 2, 3, 2, 1]),
#     'up':    (2, [0, 1, 2, 3, 2, 1]),
#     'left':  (3, [0, 1, 2, 3, 2, 1])
# }

# Example 6: Use only 2 frames for simple animation
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 1]),
#     'right': (1, [0, 1]),
#     'up':    (2, [0, 1]),
#     'left':  (3, [0, 1])
# }

# Example 7: Custom pattern (any order you want!)
# SPRITE_LAYOUT = {
#     'down':  (0, [0, 2, 4, 6]),          # Use frames 0, 2, 4, 6 (skip odd frames)
#     'right': (1, [1, 3, 5, 7]),          # Use frames 1, 3, 5, 7 (skip even frames)
#     'up':    (2, [0, 1, 2, 3, 4]),       # 5 frames
#     'left':  (3, [7, 6, 5, 4, 3, 2, 1])  # Reverse order!
# }

# Animation settings
ANIMATION_SPEED = 0.15     # Speed of animation (0.1 = slow, 0.3 = fast)

# ---------------------------------------------------------------------------
# Game meta settings
# ---------------------------------------------------------------------------
MAX_WRONG_ACCUSATIONS = 3
TOTAL_CASES = 5

# ---------------------------------------------------------------------------
# Rendering helpers / overlay content
# ---------------------------------------------------------------------------
# Grid used as a fallback when background not present
GRID_SIZE = 40
GRID_COLOR = (80, 80, 80)

# Player controls / on-screen instructions (pre-rendered in game loop)
INSTRUCTIONS = [
    "Use WASD or Arrow Keys to move",
    "Press ESC to return to menu",
]

# Path to optional background image (can be None for procedural grid)
BACKGROUND_IMAGE_PATH = "assets/images/Rusted_back.png"

