import pygame
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.menu_base import MenuBase
from utils.ui_components import Button, Slider
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR

class SettingsMenu(MenuBase):
    def __init__(self, screen, game_manager):
        super().__init__(screen)
        self.game_manager = game_manager
        self.settings = self.load_settings()
        self.background = self.load_background()
        self.setup_ui()
    
    def load_background(self):
        """Load background image from assets (same as menu)"""
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            bg_path = os.path.join(project_root, "assets", "images", "menu_background.png")
            background = pygame.image.load(bg_path)
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return background
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")
            return None
    
    def load_settings(self):
        """Load settings from file or use defaults"""
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'master_volume': 0.7,
                'music_volume': 0.8,
                'sfx_volume': 0.9,
                'fullscreen': False,
                'resolution': '1024x768'
            }
    
    def save_settings(self):
        """Save settings to file"""
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def setup_ui(self):
        # Center everything based on screen width
        center_x = SCREEN_WIDTH // 2
        
        # Sliders - positioned to the right of center
        slider_x = center_x + 80
        self.master_slider = Slider(slider_x, 255, 250, 20, 0, 1, self.settings['master_volume'])
        self.music_slider = Slider(slider_x, 305, 250, 20, 0, 1, self.settings['music_volume'])
        self.sfx_slider = Slider(slider_x, 355, 250, 20, 0, 1, self.settings['sfx_volume'])
        
        # Fullscreen button - centered
        fullscreen_text = f"Fullscreen {'ON' if self.settings['fullscreen'] else 'OFF'}"
        button_width = 280
        self.fullscreen_button = Button(center_x - button_width // 2, 450, button_width, 50,
                                      fullscreen_text, 
                                      self.font_medium, self.toggle_fullscreen, 
                                      show_icon=False)
        
        # Apply and Back buttons - centered side by side
        button_width = 200
        button_spacing = 20
        total_width = button_width * 2 + button_spacing
        start_x = center_x - total_width // 2
        
        self.apply_button = Button(start_x, 550, button_width, 50, "Apply",
                                 self.font_medium, self.apply_settings,
                                 show_icon=False)
        
        self.back_button = Button(start_x + button_width + button_spacing, 550, button_width, 50, "Back",
                                self.font_medium, self.go_back,
                                show_icon=False)
    
    def handle_input(self, event):
        self.master_slider.handle_event(event)
        self.music_slider.handle_event(event)
        self.sfx_slider.handle_event(event)
        self.fullscreen_button.handle_event(event)
        self.apply_button.handle_event(event)
        self.back_button.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.go_back()
    
    def update(self):
        self.settings['master_volume'] = self.master_slider.value
        self.settings['music_volume'] = self.music_slider.value
        self.settings['sfx_volume'] = self.sfx_slider.value
    
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
        
        title = self.font_large.render("Settings", True, COLORS['WHITE'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Center everything horizontally
        center_x = SCREEN_WIDTH // 2
        label_x = center_x - 230  # Labels to the left of center
        percent_x = center_x + 340  # Percentages to the right of sliders
        
        labels = [
            ("Master Volume", 255),
            ("Music Volume", 305),
            ("SFX Volume", 355)
        ]
        
        for label, y in labels:
            text = self.font_medium.render(label, True, COLORS['WHITE'])
            self.screen.blit(text, (label_x, y))
        
        self.master_slider.draw(self.screen)
        self.music_slider.draw(self.screen)
        self.sfx_slider.draw(self.screen)
        
        vol_texts = [
            (f"{int(self.settings['master_volume'] * 100)}%", 255),
            (f"{int(self.settings['music_volume'] * 100)}%", 305),
            (f"{int(self.settings['sfx_volume'] * 100)}%", 355)
        ]
        
        for text, y in vol_texts:
            vol_surface = self.font_medium.render(text, True, COLORS['WHITE'])
            self.screen.blit(vol_surface, (percent_x, y))
        
        self.fullscreen_button.draw(self.screen)
        self.apply_button.draw(self.screen)
        self.back_button.draw(self.screen)
    
    def toggle_fullscreen(self):
        self.settings['fullscreen'] = not self.settings['fullscreen']
        text = f"Fullscreen {'ON' if self.settings['fullscreen'] else 'OFF'}"
        self.fullscreen_button.text = text
    
    def apply_settings(self):
        self.save_settings()
        if self.settings['fullscreen']:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        print("Settings Applied!")
    
    def go_back(self):
        # Check if we came from game or main menu
        from src.game_manager import GameManagerState
        # If we have a previous state that was PLAYING, go back to game
        # Otherwise go to main menu
        if hasattr(self.game_manager, '_previous_state') and self.game_manager._previous_state == GameManagerState.PLAYING:
            self.game_manager.state = GameManagerState.PLAYING
        else:
            self.game_manager.switch_to_main_menu()