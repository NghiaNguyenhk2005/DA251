"""
Icon generator for menu buttons using Pillow
Creates beautiful, scalable icons
"""

import pygame
from PIL import Image, ImageDraw
import io

class IconGenerator:
    """Generate beautiful icons for menu buttons"""
    
    @staticmethod
    def create_play_icon(size=32, color=(255, 255, 255)):
        """Create a play button icon (triangle)"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw filled triangle
        points = [
            (size * 0.25, size * 0.2),
            (size * 0.25, size * 0.8),
            (size * 0.8, size * 0.5)
        ]
        draw.polygon(points, fill=color)
        
        return img
    
    @staticmethod
    def create_continue_icon(size=32, color=(255, 255, 255)):
        """Create a continue/resume icon (double play triangles)"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # First triangle
        points1 = [
            (size * 0.2, size * 0.2),
            (size * 0.2, size * 0.8),
            (size * 0.45, size * 0.5)
        ]
        # Second triangle
        points2 = [
            (size * 0.55, size * 0.2),
            (size * 0.55, size * 0.8),
            (size * 0.8, size * 0.5)
        ]
        
        draw.polygon(points1, fill=color)
        draw.polygon(points2, fill=color)
        
        return img
    
    @staticmethod
    def create_load_icon(size=32, color=(255, 255, 255)):
        """Create a load/folder icon"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw folder
        draw.rectangle(
            [(size * 0.15, size * 0.35), (size * 0.85, size * 0.8)],
            outline=color, width=3
        )
        
        # Draw folder tab
        draw.rectangle(
            [(size * 0.15, size * 0.2), (size * 0.45, size * 0.35)],
            outline=color, width=3
        )
        
        return img
    
    @staticmethod
    def create_settings_icon(size=32, color=(255, 255, 255)):
        """Create a settings/gear icon"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = size / 2
        radius = size * 0.25
        tooth_len = size * 0.15
        
        # Draw center circle
        draw.ellipse(
            [(center - radius, center - radius),
             (center + radius, center + radius)],
            fill=color
        )
        
        # Draw gear teeth
        import math
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            
            x1 = center + (radius + tooth_len) * math.cos(angle)
            y1 = center + (radius + tooth_len) * math.sin(angle)
            x2 = center + radius * math.cos(angle)
            y2 = center + radius * math.sin(angle)
            
            draw.line([(x2, y2), (x1, y1)], fill=color, width=3)
        
        return img
    
    @staticmethod
    def create_quit_icon(size=32, color=(255, 255, 255)):
        """Create a quit/exit icon (X)"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        margin = size * 0.2
        
        # Draw X
        draw.line(
            [(margin, margin), (size - margin, size - margin)],
            fill=color, width=4
        )
        draw.line(
            [(size - margin, margin), (margin, size - margin)],
            fill=color, width=4
        )
        
        return img
    
    @staticmethod
    def pil_to_pygame(pil_image):
        """Convert PIL image to pygame surface"""
        mode = pil_image.mode
        size = pil_image.size
        
        if mode == 'RGBA':
            raw_str = pil_image.tobytes()
            return pygame.image.fromstring(raw_str, size, mode)
        else:
            raw_str = pil_image.tobytes()
            return pygame.image.fromstring(raw_str, size, mode)
    
    @classmethod
    def get_icon(cls, icon_type, size=32, color=(255, 255, 255)):
        """Get icon as pygame surface"""
        if icon_type == "New Game":
            img = cls.create_play_icon(size, color)
        elif icon_type == "Continue":
            img = cls.create_continue_icon(size, color)
        elif icon_type == "Load Game":
            img = cls.create_load_icon(size, color)
        elif icon_type == "Settings":
            img = cls.create_settings_icon(size, color)
        elif icon_type == "Quit":
            img = cls.create_quit_icon(size, color)
        else:
            # Default empty icon
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        return cls.pil_to_pygame(img)
