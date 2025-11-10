import pygame

from interfaces import Drawable, Updatable
from .button import TextButton


class MenuPopup(Updatable, Drawable):
    def __init__(self, screen_width: int = 800, screen_height: int = 600) -> None:
        """
        Menu scene with Settings, Resume, and Quit buttons
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self._is_open: bool = False
        # Calculate center position for buttons
        center_x = screen_width // 2 - 75  # Approximate button center
        start_y = screen_height // 2 - 60
        
        # Settings button
        self.resume_button = TextButton(
            position=(center_x, start_y),
            text="Resume",
            font_size=32,
            padding=10,
            normal_bg=(70, 70, 70),
            normal_text=(255, 255, 255),
            hover_bg=(120, 120, 120),
            hover_text=(255, 255, 255),
            click_bg=(50, 50, 50),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2
        )
        
        # Resume button
        self.settings_button = TextButton(
            position=(center_x, start_y + 70),
            text="Settings",
            font_size=32,
            padding=10,
            normal_bg=(85, 85, 85),
            normal_text=(255, 255, 255),
            hover_bg=(135, 135, 135),
            hover_text=(255, 255, 255),
            click_bg=(65, 65, 65),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2
        )
        
        # Quit button
        self.quit_button = TextButton(
            position=(center_x, start_y + 140),
            text="Quit",
            font_size=32,
            padding=10,
            normal_bg=(100, 100, 100),
            normal_text=(255, 255, 255),
            hover_bg=(150, 150, 150),
            hover_text=(255, 255, 255),
            click_bg=(80, 80, 80),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2
        )

    def toggle(self):
        if self.is_open():
            self._is_open = False
        else:
            self._is_open = True

    def is_open(self) -> bool:
        return self._is_open
    
    def update(self, delta_time: float = 0):
        """Update menu scene state"""
        # Update button states
        self.resume_button.update()
        self.settings_button.update()
        self.quit_button.update()
        
        # Check for button clicks
        if self.resume_button.was_clicked():
            self.toggle()

    def handle_event(self, event: pygame.event.Event):
        pass

    def draw(self, screen: pygame.Surface):
        """Draw all menu buttons"""
        if self._is_open:
            self.settings_button.draw(screen)
            self.resume_button.draw(screen)
            self.quit_button.draw(screen)
