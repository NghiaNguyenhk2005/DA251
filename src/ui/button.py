from abc import abstractmethod
import pygame

from interfaces import Drawable, Updatable

class IButton:
    @abstractmethod
    def was_clicked(self) -> bool: return False
    def is_pressed(self) -> bool: return False

class Button(IButton, Drawable, Updatable):
    """Interactive button with hover and click states using sprite frames"""
    
    def __init__(self, position: tuple[int, int], image: pygame.Surface, scale: int=1, split: int=5) -> None:
        """
        Initialize a button with sprite-based animation frames
        
        Args:
            position: (x, y) position of the button on screen
            image: Sprite sheet containing button frames (normal, hover, clicked)
            scale: Scale factor to resize the button image
            split: Number of frames in the sprite sheet (default: 5)
        """
        self.frame = 0
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.frame_width = self.image.get_width() // split
        self.frame_height = self.image.get_height()
        self.rect = pygame.Rect(position[0], position[1], self.frame_width, self.frame_height)
        self._is_hover = False
        self._is_pressed = False
        self._was_clicked = False

    def update(self, delta_time: float = 0):
        """
        Update button state based on mouse interaction
        
        Updates the button state based on hover and click:
        - Checks if mouse is hovering
        - Detects clicks (edge-triggered)
        - Updates frame for visual state
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.frame = 1
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]:
                self.frame = 2
                if not self._was_clicked:
                    self._is_pressed = True
                    self._was_clicked = True
                else:
                    self._is_pressed = False
            else:
                self._is_pressed = False
                self._was_clicked = False
        else: 
            self.frame = 0
            self._is_pressed = False
            self._is_hover = False
            self._was_clicked = False

    def draw(self, screen: pygame.Surface):
        """
        Draw the button with current state
        
        Draws the button frame based on current state:
        - Frame 0: Normal state
        - Frame 1: Hover state
        - Frame 2: Clicked state
        
        Args:
            screen: Game's Screen - Surface to draw the button on
        """
        source_rect = pygame.Rect(self.frame * self.frame_width, 0, self.frame_width, self.frame_height)
        screen.blit(self.image, self.rect, source_rect)

    def handle_event(self, event: pygame.event.Event):
        pass

    def is_hover(self):
        """
        Check if the mouse is hovering over the button
        
        Returns:
            bool: True if mouse is hovering, False otherwise
        """
        return self._is_hover

    def is_pressed(self):
        """
        Check if the button is currently being clicked (level-based - True while held down)
        
        For edge detection (single-fire events), use _was_clicked attribute or was_clicked() method.
        was_clicked is True only on the first frame of the click, not while held.
        
        Returns:
            bool: True if button is clicked, False otherwise
        """
        return self._is_pressed
    
    def was_clicked(self):
        """
        Check if the button was just clicked (edge detection - True only on first frame)
        
        This is useful for single-fire events like toggling, opening dialogs, etc.
        Returns True only on the initial click, not while the button is held down.
        
        Returns:
            bool: True if button was just clicked (first frame only), False otherwise
        """
        return self._was_clicked


class TextButton(IButton, Drawable, Updatable):
    """Interactive text button with hover and click states"""
    
    def __init__(self, position: tuple[int, int], text: str, font_size: int = 32,
                 padding: int = 10,
                 normal_bg: tuple[int, int, int] = (100, 100, 100),
                 normal_text: tuple[int, int, int] = (255, 255, 255),
                 hover_bg: tuple[int, int, int] = (150, 150, 150),
                 hover_text: tuple[int, int, int] = (255, 255, 255),
                 click_bg: tuple[int, int, int] = (80, 80, 80),
                 click_text: tuple[int, int, int] = (200, 200, 200),
                 border_color: tuple[int, int, int] = (200, 200, 200),
                 border_width: int = 2,
                 border_radius: int = 10) -> None:
        """
        Initialize a text button with color-based state visualization
        
        Args:
            position: (x, y) position of the button on screen
            text: Text to display on the button
            font_size: Font size for the button text
            padding: Padding around the text
            normal_bg: Background color in normal state (RGB)
            normal_text: Text color in normal state (RGB)
            hover_bg: Background color in hover state (RGB)
            hover_text: Text color in hover state (RGB)
            click_bg: Background color in clicked state (RGB)
            click_text: Text color in clicked state (RGB)
            border_color: Border color (RGB)
            border_width: Width of the border
            border_radius: Radius of the rounded corners
        """
        self.position = position
        self.text = text
        self.font_size = font_size
        self.padding = padding
        
        # State colors
        self.normal_bg = normal_bg
        self.normal_text = normal_text
        self.hover_bg = hover_bg
        self.hover_text = hover_text
        self.click_bg = click_bg
        self.click_text = click_text
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        
        # Create font and render text surfaces for each state
        self.font = pygame.font.Font(None, font_size)
        self.text_surface_normal = self.font.render(text, True, normal_text)
        self.text_surface_hover = self.font.render(text, True, hover_text)
        self.text_surface_click = self.font.render(text, True, click_text)
        
        # Calculate button dimensions
        text_width = self.text_surface_normal.get_width()
        text_height = self.text_surface_normal.get_height()
        self.rect = pygame.Rect(position[0], position[1], 
                               text_width + padding * 2, 
                               text_height + padding * 2)
        
        self._is_hover = False
        self._is_pressed = False
        self._was_clicked = False
        
        # Current visual state
        self._current_bg = normal_bg
        self._current_text_surface = self.text_surface_normal

    def update(self, delta_time: float = 0):
        """
        Update button state based on mouse interaction
        
        Updates the button state and visual appearance based on hover and click
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state
        if self.rect.collidepoint(mouse_pos):
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]:
                self._current_bg = self.click_bg
                self._current_text_surface = self.text_surface_click
                if not self._was_clicked:
                    self._is_pressed = True
                    self._was_clicked = True
                else:
                    self._is_pressed = False
            else:
                self._current_bg = self.hover_bg
                self._current_text_surface = self.text_surface_hover
                self._is_pressed = False
                self._was_clicked = False
        else:
            self._current_bg = self.normal_bg
            self._current_text_surface = self.text_surface_normal
            self._is_hover = False
            self._is_pressed = False
            self._was_clicked = False

    def handle_event(self, event: pygame.event.Event):
        pass

    def draw(self, screen: pygame.Surface):
        """
        Draw the text button with current state
        
        Draws the button appearance based on current state:
        - Normal state: normal_bg and normal_text colors
        - Hover state: hover_bg and hover_text colors
        - Clicked state: click_bg and click_text colors
        
        Args:
            screen: Game's Screen - Surface to draw the button on
        """
        # Draw background with rounded corners
        pygame.draw.rect(screen, self._current_bg, self.rect, border_radius=self.border_radius)
        
        # Draw border with rounded corners
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
        
        # Draw text centered in button
        text_x = self.rect.x + self.padding
        text_y = self.rect.y + self.padding
        screen.blit(self._current_text_surface, (text_x, text_y))

    def is_hover(self):
        """
        Check if the mouse is hovering over the button
        
        Returns:
            bool: True if mouse is hovering, False otherwise
        """
        return self._is_hover

    def is_pressed(self):
        """
        Check if the button is currently being clicked (level-based - True while held down)
        
        For edge detection (single-fire events), use _was_clicked attribute or was_clicked() method.
        was_clicked is True only on the first frame of the click, not while held.
        
        Returns:
            bool: True if button is clicked, False otherwise
        """
        return self._is_pressed
    
    def was_clicked(self):
        """
        Check if the button was just clicked (edge detection - True only on first frame)
        
        This is useful for single-fire events like toggling, opening dialogs, etc.
        Returns True only on the initial click, not while the button is held down.
        
        Returns:
            bool: True if button was just clicked (first frame only), False otherwise
        """
        return self._was_clicked
