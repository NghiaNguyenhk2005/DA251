import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.menu_base import MenuBase
from utils.ui_components import Button
from utils.text_effects import TextRenderer, TITLE_COLORS, GLOW_COLORS
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR

class MainMenu(MenuBase):
    def __init__(self, screen, game_manager):
        super().__init__(screen)
        self.game_manager = game_manager
        self.items = ["New Game", "Continue", "Settings", "Quit"]
        self.background = self.load_background()
        self.text_renderer = TextRenderer()
        self.title_surface = None
        self.title_rect = None
        self.render_title()
        self.setup_buttons()
    
    def setup_buttons(self):
        self.buttons = []
        button_width = 280   # Increased from 240
        button_height = 60   # Increased from 50
        # Adjust start_y to account for title
        start_y = SCREEN_HEIGHT // 2 - (len(self.items) * 75) // 2 + 80  # Adjusted spacing
        
        for i, item in enumerate(self.items):
            x = SCREEN_WIDTH // 2 - button_width // 2
            y = start_y + i * 75  # Adjusted spacing between buttons
            action = self.get_action(item)
            button = Button(x, y, button_width, button_height, item, self.font_medium, action)
            self.buttons.append(button)
    
    def load_background(self):
        """Load background image from assets"""
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            bg_path = os.path.join(project_root, "assets", "images", "menu_background.png")
            background = pygame.image.load(bg_path)
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return background
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")
            return None
    
    def render_title(self):
        """Render title with glow effect"""
        # Use render_glow_text for better visual effect
        self.title_surface, self.title_rect = self.text_renderer.render_glow_text(
            text="SEVEN DEADLY SINS",
            color=(180, 140, 60),      # Muted, darker, matte color
            glow_color=(120, 80, 0),   # Dark brownish glow for darker atmosphere
            font_size=56,              # Reduced from 72 for more compact size
            screen_width=SCREEN_WIDTH,
            glow_amount=3,             # Reduced glow layers for more subtle effect
            letter_spacing=-5,         # Tight spacing between letters
            word_spacing=20            # Reduce space between words (SEVEN DEADLY SINS)
        )
        # Position title higher with more padding from top
        self.title_rect.y = 60  # Reduced from 80 to move title higher
    
    def get_action(self, item):
        actions = {
            "New Game": self.new_game,
            "Continue": self.continue_game,
            "Load Game": self.load_game,
            "Settings": self.settings,
            "Quit": self.quit_game
        }
        return actions.get(item)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.navigate_up()
                self.update_button_selection()
            elif event.key == pygame.K_DOWN:
                self.navigate_down()
                self.update_button_selection()
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected_index].action()
        
        for button in self.buttons:
            button.handle_event(event)
    
    def update_button_selection(self):
        for i, button in enumerate(self.buttons):
            button.is_selected = (i == self.selected_index)
    
    def update(self):
        pass
    
    def draw(self):
        # Draw background image
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(COLORS['BLACK'])
        
        # Create semi-transparent overlay for better text visibility
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Draw title with glow effect
        if self.title_surface and self.title_rect:
            self.screen.blit(self.title_surface, self.title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
    
    def new_game(self):
        self.game_manager.start_new_game()
    
    def continue_game(self):
        pass
    
    def load_game(self):
        self.game_manager.switch_to_load_menu()
    
    def settings(self):
        self.game_manager.switch_to_settings()
    
    def quit_game(self):
        pygame.quit()
        sys.exit()