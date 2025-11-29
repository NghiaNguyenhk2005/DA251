import pygame

class Button:
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
        self._is_clicked = False

    def draw(self, screen: pygame.Surface):
        """
        Draw the button and update its state based on mouse interaction
        
        Updates the button frame based on hover and click states:
        - Frame 0: Normal state
        - Frame 1: Hover state
        - Frame 2: Clicked state
        
        Args:
            screen: Surface to draw the button on
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.frame = 1
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]: 
                self.frame = 2
                self._is_clicked = True
        else: 
            self.frame = 0
            self._is_clicked = False
            self._is_hover = False
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
