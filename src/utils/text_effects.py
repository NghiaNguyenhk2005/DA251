# src/utils/text_effects.py
import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import COLORS

class TextRenderer:
    """Utility class for rendering text with effects"""
    
    def __init__(self):
        self.pixel_font_large = self.load_pixel_font(72)
        self.pixel_font_medium = self.load_pixel_font(48)
        self.pixel_font_small = self.load_pixel_font(32)
        self._font_type = self._detect_font_type()
    
    def _detect_font_type(self):
        """Detect which font type is being used"""
        if self.pixel_font_large:
            font_name = str(self.pixel_font_large.name) if hasattr(self.pixel_font_large, 'name') else ""
            if 'monospace' in font_name.lower():
                return "monospace (fallback)"
            else:
                return "pixel font"
        return "unknown"
    
    def load_pixel_font(self, size):
        """Load pixel font or fallback to default monospace"""
        try:
            # Get assets directory
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                     "assets/fonts")
            
            # Try to find pixel font from assets with multiple possible names
            font_names = [
                "pixel.ttf",
                "PressStart2P.ttf", 
                "Press Start 2P.ttf",
                "pixelated.ttf",
                "Pixelated.ttf",
                "pixelated-bold.ttf",
                "joystix.ttf",
                "Joystix.ttf",
            ]
            
            # Check each possible font name
            for font_name in font_names:
                font_path = os.path.join(assets_dir, font_name)
                if os.path.exists(font_path):
                    try:
                        loaded_font = pygame.font.Font(font_path, size)
                        print(f"✓ Loaded pixel font: {font_name}")
                        return loaded_font
                    except Exception as e:
                        print(f"⚠ Font {font_name} couldn't be loaded: {e}")
                        continue
            
            # Fallback to monospace if no pixel font found
            # Use 'couriernew' or 'consolas' for better appearance, fallback to monospace
            system_fonts = ['couriernew', 'consolas', 'courier', 'monospace']
            for font_name in system_fonts:
                try:
                    return pygame.font.SysFont(font_name, size, bold=True)
                except:
                    continue
            
            # Last resort
            return pygame.font.SysFont('monospace', size, bold=True)
            
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            return pygame.font.SysFont('monospace', size, bold=True)
    
    def render_title(self, text, color=(255, 255, 100), screen_width=1024):
        """
        Render game title with shadow effect
        
        Args:
            text: Title text
            color: RGB color tuple (default: pale yellow)
            screen_width: Screen width for centering
        
        Returns:
            (surface, rect) tuple for blitting
        """
        # Create shadow text (dark version)
        shadow_text = self.pixel_font_large.render(text, True, (20, 20, 20))
        shadow_rect = shadow_text.get_rect()
        
        # Create main text
        main_text = self.pixel_font_large.render(text, True, color)
        main_rect = main_text.get_rect()
        
        # Create combined surface with shadow effect
        combined_width = main_rect.width + 8
        combined_height = main_rect.height + 8
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)
        
        # Draw shadow offset
        combined_surface.blit(shadow_text, (4, 4))
        # Draw main text
        combined_surface.blit(main_text, (0, 0))
        
        combined_rect = combined_surface.get_rect(center=(screen_width // 2, 0))
        
        return combined_surface, combined_rect
    
    def render_glow_text(self, text, color=(255, 255, 100), glow_color=(255, 200, 0), 
                        font_size=72, screen_width=1024, glow_amount=3, letter_spacing=0, word_spacing=0):
        """
        Render text with glow effect and optional letter/word spacing
        
        Args:
            text: Text to render
            color: Main text color
            glow_color: Glow color
            font_size: Font size
            screen_width: Screen width
            glow_amount: Number of glow layers
            letter_spacing: Space between letters (negative to compress)
            word_spacing: Space reduction for words (negative to compress between words)
        
        Returns:
            (surface, rect) tuple
        """
        font = self.load_pixel_font(font_size)
        
        # Render individual characters for custom letter spacing
        if letter_spacing != 0 or word_spacing != 0:
            # Split text into words and process spacing
            words = text.split(' ')
            word_surfaces = []
            
            for word in words:
                # Render each character in word with letter_spacing
                char_surfaces = []
                char_width = 0
                for char in word:
                    char_surf = font.render(char, True, color)
                    char_surfaces.append(char_surf)
                    char_width += char_surf.get_width() + (letter_spacing if char != word[-1] else 0)
                
                # Create word surface
                if char_surfaces:
                    word_height = max(surf.get_height() for surf in char_surfaces)
                    word_surf = pygame.Surface((char_width, word_height), pygame.SRCALPHA)
                    
                    x_pos = 0
                    for i, char_surf in enumerate(char_surfaces):
                        word_surf.blit(char_surf, (x_pos, 0))
                        if i < len(char_surfaces) - 1:
                            x_pos += char_surf.get_width() + letter_spacing
                        else:
                            x_pos += char_surf.get_width()
                    
                    word_surfaces.append(word_surf)
            
            # Calculate total width with word spacing
            total_width = sum(ws.get_width() for ws in word_surfaces)
            total_width += (len(word_surfaces) - 1) * (font.get_height() // 3 + word_spacing)  # Default space width + word_spacing
            max_height = max(ws.get_height() for ws in word_surfaces) if word_surfaces else 0
            
            glow_width = total_width + (glow_amount * 2) * 2
            glow_height = max_height + (glow_amount * 2) * 2
            glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
            
            # Draw glow for words
            for layer in range(glow_amount, 0, -1):
                x_offset = glow_amount * 2 - layer
                y_offset = glow_amount * 2 - layer
                current_x = x_offset
                alpha = int(255 * (1 - layer / glow_amount) * 0.3)
                
                for word_idx, word in enumerate(words):
                    for char_idx, char in enumerate(word):
                        glow_char = font.render(char, True, (*glow_color, alpha))
                        glow_surface.blit(glow_char, (current_x, y_offset))
                        current_x += glow_char.get_width() + (letter_spacing if char_idx < len(word) - 1 else 0)
                    
                    if word_idx < len(words) - 1:
                        current_x += font.get_height() // 3 + word_spacing
            
            # Draw main text
            current_x = glow_amount
            for word_idx, word in enumerate(words):
                for char_idx, char in enumerate(word):
                    char_surf = font.render(char, True, color)
                    glow_surface.blit(char_surf, (current_x, glow_amount))
                    current_x += char_surf.get_width() + (letter_spacing if char_idx < len(word) - 1 else 0)
                
                if word_idx < len(words) - 1:
                    current_x += font.get_height() // 3 + word_spacing
        else:
            # Original behavior - single render
            main_text = font.render(text, True, color)
            main_rect = main_text.get_rect()
            
            glow_width = main_rect.width + (glow_amount * 2) * 2
            glow_height = main_rect.height + (glow_amount * 2) * 2
            glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
            
            # Draw glow layers
            for i in range(glow_amount, 0, -1):
                glow_text = font.render(text, True, (*glow_color, int(255 * (1 - i / glow_amount) * 0.3)))
                offset = glow_amount * 2 - i
                glow_surface.blit(glow_text, (offset, offset))
            
            # Draw main text in center
            glow_surface.blit(main_text, (glow_amount, glow_amount))
        
        glow_rect = glow_surface.get_rect(center=(screen_width // 2, 0))
        
        return glow_surface, glow_rect
    
    def render_subtitle(self, text, color=(200, 200, 200), screen_width=1024):
        """Render subtitle text"""
        subtitle = self.pixel_font_medium.render(text, True, color)
        subtitle_rect = subtitle.get_rect(center=(screen_width // 2, 0))
        
        return subtitle, subtitle_rect


# Color presets
TITLE_COLORS = {
    'pale_yellow': (255, 255, 150),
    'gold': (255, 215, 0),
    'neon_yellow': (255, 255, 0),
    'warm_yellow': (255, 245, 150),
    'pale_gold': (255, 250, 200),
    'crimson': (220, 20, 60),
    'neon_pink': (255, 0, 255),
}

GLOW_COLORS = {
    'yellow': (255, 200, 0),
    'gold': (255, 180, 0),
    'red': (255, 0, 0),
    'purple': (200, 0, 200),
}
