"""main
Entry point and top-level game loop / orchestration.

Responsibilities:
    - Initialize pygame & window
    - Manage high-level game states
    - Dispatch events to subsystems (menu, player)
    - Coordinate draw cycle (background, scene, overlays)

Rendering is decomposed into small helper methods for clarity and
future extension (e.g., adding dialogue / inventory screens).
"""

import pygame
import sys
import config as cfg
from src.player import Player
from src.game_states import GameState, StateManager
from src.ui import Menu

class Game:
    """Main game class with state management"""
    
    def __init__(self):
        """Initialize the game"""
        # Initialize Pygame
        pygame.init()
        
        # Create the game window
        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pygame.display.set_caption(cfg.TITLE)
        
        # Create a clock to control frame rate
        self.clock = pygame.time.Clock()
        
        # Game state flag
        self.running = True
        
        # State management
        self.state_manager = StateManager()
        
        # Load background image
        self.background = None
        if cfg.BACKGROUND_IMAGE_PATH:
            try:
                raw_bg = pygame.image.load(cfg.BACKGROUND_IMAGE_PATH).convert()
                self.background = pygame.transform.scale(
                    raw_bg, (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
                )
            except pygame.error as e:
                print(f"Warning: Could not load background image: {e}")
        
        # Create player (will be shown when playing)
        self.player = Player(
            cfg.SCREEN_WIDTH // 2 - cfg.PLAYER_SIZE // 2,
            cfg.SCREEN_HEIGHT // 2 - cfg.PLAYER_SIZE // 2,
        )
        
        # Create main menu
        self.main_menu = Menu(
            "Se7en Detective",
            [
                ("Start Game", self.start_game),
                ("Quit", self.quit_game),
            ],
        )
        
        print("Game initialized successfully!")
    
    def start_game(self):
        """Start the game"""
        self.state_manager.change_state(GameState.PLAYING)
    
    def quit_game(self):
        """Quit the game"""
        self.running = False
    
    def handle_events(self):
        """Handle user input and events"""
        for event in pygame.event.get():
            # Check if user closed the window
            if event.type == pygame.QUIT:
                self.running = False
            
            # Check for key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to menu from game
                    if self.state_manager.is_state(GameState.PLAYING):
                        self.state_manager.change_state(GameState.MENU)
                    else:
                        self.running = False
            
            # Handle menu events
            if self.state_manager.is_state(GameState.MENU):
                self.main_menu.handle_event(event)
        
        # Handle player input when playing
        if self.state_manager.is_state(GameState.PLAYING):
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
    
    def update(self):
        """Update game logic"""
        if self.state_manager.is_state(GameState.PLAYING):
            self.player.update()
    
    def _draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            for x in range(0, cfg.SCREEN_WIDTH, cfg.GRID_SIZE):
                pygame.draw.line(
                    self.screen, cfg.GRID_COLOR, (x, 0), (x, cfg.SCREEN_HEIGHT)
                )
            for y in range(0, cfg.SCREEN_HEIGHT, cfg.GRID_SIZE):
                pygame.draw.line(
                    self.screen, cfg.GRID_COLOR, (0, y), (cfg.SCREEN_WIDTH, y)
                )

    def _draw_menu(self):
        self.main_menu.draw(self.screen)

    def _draw_play_scene(self):
        self._draw_background()
        self.player.draw(self.screen)
        # Instruction overlay
        if not hasattr(self, "_instruction_font"):
            self._instruction_font = pygame.font.Font(None, 24)
            self._cached_instructions = [
                self._instruction_font.render(text, True, cfg.WHITE)
                for text in cfg.INSTRUCTIONS
            ]
        for i, surf in enumerate(self._cached_instructions):
            self.screen.blit(surf, (10, 10 + i * 25))
        # Player position (debug)
        pos_surface = self._instruction_font.render(
            f"Position: ({int(self.player.x)}, {int(self.player.y)})", True, cfg.YELLOW
        )
        self.screen.blit(pos_surface, (10, cfg.SCREEN_HEIGHT - 30))

    def draw(self):
        """Composite frame renderer"""
        self.screen.fill(cfg.DARK_GRAY)
        if self.state_manager.is_state(GameState.MENU):
            self._draw_menu()
        elif self.state_manager.is_state(GameState.PLAYING):
            self._draw_play_scene()
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(cfg.FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()

# Entry point of the program
if __name__ == "__main__":
    game = Game()
    game.run()
