import pygame
from typing import Optional
from .i_scene import IScene


class OfficeScene(IScene):
    def __init__(self, screen_width: int = 800, screen_height: int = 600) -> None:
        """
        Office scene with background image
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load and scale background
        self.background = pygame.image.load("assets/images/office.png")
        self.background = pygame.transform.scale(
            self.background, 
            (screen_width, screen_height)
        )
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events for this scene"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Handle exit or return to map
                pass
    
    def update(self) -> None:
        """Update scene state"""
        pass
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the scene"""
        screen.blit(self.background, (0, 0))
