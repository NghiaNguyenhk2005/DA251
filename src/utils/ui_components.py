import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(__file__))
from config import COLORS

try:
    from icon_generator import IconGenerator
except ImportError:
    from utils.icon_generator import IconGenerator

class Button:
    """Button with rounded corners and beautiful icons"""
    
    def __init__(self, x, y, width, height, text, font, action=None, show_icon=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.is_hovered = False
        self.is_selected = False
        self.border_radius = 15  # Rounded corners radius
        self.show_icon = show_icon
        
        # Pre-generate icon if needed
        if self.show_icon:
            self.icon = IconGenerator.get_icon(text, size=28, color=(255, 255, 255))
            self.icon_rect = self.icon.get_rect()
        else:
            self.icon = None
            self.icon_rect = None
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
    
    def draw_rounded_rect(self, screen, color, border_color=None, border_width=2):
        """Draw a rectangle with rounded corners and pixel art style"""
        # Draw main rectangle with pixelated look
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        
        # Draw multiple borders for pixel art depth effect
        if border_color:
            # Outer border
            pygame.draw.rect(screen, border_color, self.rect, border_width, border_radius=self.border_radius)
            
            # Add inner highlight for 3D pixel effect
            inner_rect = pygame.Rect(
                self.rect.x + border_width + 1,
                self.rect.y + border_width + 1,
                self.rect.width - (border_width + 1) * 2,
                self.rect.height - (border_width + 1) * 2
            )
            highlight_color = tuple(min(255, c + 30) for c in color)
            pygame.draw.rect(screen, highlight_color, inner_rect, 1, border_radius=self.border_radius - 2)
            
            # Add bottom shadow for depth
            shadow_rect = pygame.Rect(
                self.rect.x + 2,
                self.rect.y + self.rect.height - 4,
                self.rect.width - 4,
                2
            )
            shadow_color = tuple(max(0, c - 40) for c in color)
            pygame.draw.rect(screen, shadow_color, shadow_rect)
    
    def draw(self, screen):
        # Determine colors based on state - pixel art color palette
        if self.is_selected:
            bg_color = (80, 120, 180)   # Pixel blue highlight
            border_color = (120, 180, 255)
        elif self.is_hovered:
            bg_color = (90, 90, 90)     # Pixel gray hover
            border_color = (180, 180, 180)
        else:
            bg_color = (60, 60, 60)     # Dark pixel gray background
            border_color = (120, 120, 120)
        
        # Draw rounded button background with pixel style
        self.draw_rounded_rect(screen, bg_color, border_color, border_width=3)
        
        # Check if text has multiple lines
        if '\n' in self.text:
            # Multi-line text (for save slots)
            lines = self.text.split('\n')
            line_height = self.font.get_height() + 4  # Increased spacing between lines
            total_height = len(lines) * line_height
            
            # Start from center, properly aligned
            start_y = self.rect.centery - total_height // 2 + line_height // 2
            
            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, COLORS['WHITE'])
                text_rect = text_surface.get_rect(centerx=self.rect.centerx, centery=start_y + i * line_height)
                screen.blit(text_surface, text_rect)
        elif self.show_icon and self.icon:
            # Single-line text with icon
            text_surface = self.font.render(self.text, True, COLORS['WHITE'])
            icon_width = self.icon_rect.width
            text_width = text_surface.get_width()
            spacing = 15  # Space between icon and text
            
            total_width = icon_width + spacing + text_width
            
            # Calculate starting x position to center the combined elements
            start_x = self.rect.centerx - (total_width // 2)
            
            # Draw icon (centered vertically and horizontally with text)
            icon_x = start_x
            icon_y = self.rect.centery - self.icon_rect.height // 2
            screen.blit(self.icon, (icon_x, icon_y))
            
            # Draw text (centered vertically, positioned to the right of icon)
            text_x = start_x + icon_width + spacing
            text_y = self.rect.centery - text_surface.get_height() // 2
            screen.blit(text_surface, (text_x, text_y))
        else:
            # Text only, centered (no icon)
            text_surface = self.font.render(self.text, True, COLORS['WHITE'])
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            relative_x = event.pos[0] - self.rect.x
            self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.max_val, self.value))
    
    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['DARK_GRAY'], self.rect)
        
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, COLORS['WHITE'], handle_rect)