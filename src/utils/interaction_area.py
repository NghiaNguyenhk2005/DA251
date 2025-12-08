import pygame
from typing import Callable

class InteractionArea:
    """
    Represents a 2D area that a player can enter and interact with.
    When the player is inside, it displays an "[F]" prompt and listens for
    an interaction key press to trigger a callback function.
    """
    def __init__(self, rect: pygame.Rect, callback: Callable):
        """
        Initializes the InteractionArea.

        Args:
            rect: A pygame.Rect defining the trigger area.
            callback: The function to call when the interaction is triggered.
        """
        self.rect = rect
        self.callback = callback
        self.player_is_inside = False

        # Basic font and render for the "[F]" prompt
        try:
            self.font = pygame.font.Font("src/assets/fonts/Harmonic.ttf", 32)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 36)
            
        self.text_surface = self.font.render("[F]", True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()
        
        # Simple background for better visibility
        self.text_background = pygame.Surface(
            (self.text_rect.width + 10, self.text_rect.height + 10),
            pygame.SRCALPHA
        )
        self.text_background.fill((0, 0, 0, 180)) # Semi-transparent black

    def update(self, player_rect: pygame.Rect):
        """
        Checks for player collision with the area and updates the internal state.
        This should be called every frame.
        """
        self.player_is_inside = self.rect.colliderect(player_rect)

    def handle_event(self, event: pygame.event.Event):
        """
        Handles the interaction event (e.g., key press).
        If the player is inside and presses the interaction key, trigger the callback.
        """
        if self.player_is_inside and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.callback()

    def draw(self, screen: pygame.Surface, player_rect: pygame.Rect):
        """
        Draws the "[F]" indicator above the player's head if they are inside the area.
        """
        if self.player_is_inside:
            # Position text and background above the player's head
            bg_rect = self.text_background.get_rect()
            bg_rect.centerx = player_rect.centerx
            bg_rect.bottom = player_rect.top - 10
            
            self.text_rect.center = bg_rect.center

            screen.blit(self.text_background, bg_rect)
            screen.blit(self.text_surface, self.text_rect)

    def draw_debug(self, screen: pygame.Surface):
        """
        Draws the boundary of the interaction area for debugging purposes.
        """
        # Draw with a unique color to distinguish from obstacle rects
        debug_color = (0, 255, 255, 150) # Cyan
        debug_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        debug_surface.fill(debug_color)
        screen.blit(debug_surface, self.rect.topleft)
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)
