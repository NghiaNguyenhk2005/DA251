import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from abc import ABC, abstractmethod
from config import COLORS, MENU_FONT_SIZE, BUTTON_FONT_SIZE

class MenuBase(ABC):
    
    def __init__(self, screen):
        self.screen = screen
        # Load pixel font for menu buttons
        self.font_large = self.load_pixel_font(MENU_FONT_SIZE)
        self.font_medium = self.load_pixel_font(BUTTON_FONT_SIZE)
        self.selected_index = 0
        self.items = []
    
    def load_pixel_font(self, size):
        """Load pixel font or fallback to default"""
        try:
            # Try to find pixel font from assets
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "assets/fonts")
            
            font_names = [
                "PressStart2P.ttf", 
                "pixel.ttf",
                "Pixelated.ttf",
            ]
            
            for font_name in font_names:
                font_path = os.path.join(assets_dir, font_name)
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            
            # Fallback to system font
            return pygame.font.Font(None, size)
        except:
            return pygame.font.Font(None, size)
        
    @abstractmethod
    def handle_input(self, event):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass
    
    def navigate_up(self):
        self.selected_index = (self.selected_index - 1) % len(self.items)
    
    def navigate_down(self):
        self.selected_index = (self.selected_index + 1) % len(self.items)