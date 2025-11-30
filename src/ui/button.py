import pygame
from typing import Optional, Callable, Tuple, Any

class Button:
    """Interactive button with hover and click states using sprite frames"""
    
    def __init__(self, position: tuple[int, int], image: pygame.Surface, scale: int=1, split: int=5, on_click: Optional[Callable[[], None]] = None) -> None:
        """
        Initialize a button with sprite-based animation frames
        
        Args:
            position: (x, y) position of the button on screen
            image: Sprite sheet containing button frames (normal, hover, clicked)
            scale: Scale factor to resize the button image
            split: Number of frames in the sprite sheet (default: 5)
            on_click: Callback function when button is clicked
        """
        self.frame = 0
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.frame_width = self.image.get_width() // split
        self.frame_height = self.image.get_height()
        self.rect = pygame.Rect(position[0], position[1], self.frame_width, self.frame_height)
        self._is_hover = False
        self._is_clicked = False
        self.on_click = on_click

    def update(self):
        """
        Update the button state based on mouse interaction
        
        Updates the button frame based on hover and click states:
        - Frame 0: Normal state
        - Frame 1: Hover state
        - Frame 2: Clicked state
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.frame = 1
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]: 
                self.frame = 2
                self._is_clicked = True
            else:
                if self._is_clicked:
                    # Mouse released inside button
                    if self.on_click:
                        self.on_click()
                    self._is_clicked = False
        else: 
            self.frame = 0
            self._is_clicked = False
            self._is_hover = False

    def draw(self, screen: pygame.Surface):
        """
        Draw the button
        
        Args:
            screen: Surface to draw the button on
        """
        source_rect = pygame.Rect(self.frame * self.frame_width, 0, self.frame_width, self.frame_height)
        screen.blit(self.image, self.rect, source_rect)

    def is_hover(self):
        """
        Check if the mouse is hovering over the button
        
        Returns:
            bool: True if mouse is hovering, False otherwise
        """
        return self._is_hover

    def is_clicked(self):
        """
        Check if the button is currently being clicked
        
        Returns:
            bool: True if button is clicked, False otherwise
        """
        return self._is_clicked

class TextButton:
    """Button with text label and background colors"""
    
    def __init__(self, 
                 position: Tuple[int, int], 
                 text: str, 
                 font_size: int = 32, 
                 padding: int = 10, 
                 normal_bg: Tuple[int, int, int] = (100, 100, 100), 
                 normal_text: Tuple[int, int, int] = (255, 255, 255), 
                 hover_bg: Tuple[int, int, int] = (150, 150, 150), 
                 hover_text: Tuple[int, int, int] = (255, 255, 255), 
                 click_bg: Tuple[int, int, int] = (80, 80, 80), 
                 click_text: Tuple[int, int, int] = (200, 200, 200), 
                 border_color: Tuple[int, int, int] = (200, 200, 200), 
                 border_width: int = 2,
                 on_click: Optional[Callable[[], None]] = None) -> None:
        
        self.position = position
        self.text = text
        self.font_size = font_size
        self.padding = padding
        self.normal_bg = normal_bg
        self.normal_text = normal_text
        self.hover_bg = hover_bg
        self.hover_text = hover_text
        self.click_bg = click_bg
        self.click_text = click_text
        self.border_color = border_color
        self.border_width = border_width
        self.on_click = on_click
        
        self.font = pygame.font.Font(None, self.font_size)
        
        self._is_hover = False
        self._is_clicked = False
        
        self._update_rect()

    def _update_rect(self):
        text_surf = self.font.render(self.text, True, self.normal_text)
        self.width = text_surf.get_width() + self.padding * 2
        self.height = text_surf.get_height() + self.padding * 2
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self._is_hover = self.rect.collidepoint(mouse_pos)
        
        if self._is_hover:
            if pygame.mouse.get_pressed()[0]:
                self._is_clicked = True
            else:
                if self._is_clicked:
                    # Mouse released
                    if self.on_click:
                        self.on_click()
                    self._is_clicked = False
        else:
            self._is_clicked = False

    def draw(self, screen: pygame.Surface):
        # Determine colors
        if self._is_clicked:
            bg_color = self.click_bg
            text_color = self.click_text
        elif self._is_hover:
            bg_color = self.hover_bg
            text_color = self.hover_text
        else:
            bg_color = self.normal_bg
            text_color = self.normal_text
            
        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect)
        
        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
            
        # Draw text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
