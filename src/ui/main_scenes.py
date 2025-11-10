import pygame

from typing import Optional, Callable

from interfaces import Drawable, Updatable
from .button import Button
from .map_button import MapButton
from .menu_popup import MenuPopup

MAIN_MENU_IMG = "assets/images/ui/menu-button.png"
MAP_IMG = "assets/images/ui/map-button.png"
JOURNAL_IMG = "assets/images/ui/journal-button.png"
MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"


class MainSceneUi(Updatable, Drawable):
    def __init__(self, screen_width: int = 800, screen_height: int = 600) -> None:
        """
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
        """
        menu_img = pygame.image.load(MAIN_MENU_IMG)
        journal_img = pygame.image.load(JOURNAL_IMG)
        map_img = pygame.image.load(MAP_IMG)
        self.menu_popup: MenuPopup = MenuPopup(screen_width=screen_width, screen_height=screen_height)

        self.menu_button = Button(position=(10, 10), image=menu_img, scale=2, split=3)
        self.map_button = MapButton(
            position=(10, self.menu_button.rect.bottom + 10), 
            image=map_img, 
            screen_width=screen_width, 
            screen_height=screen_height,
            scale=2, 
            split=3,
        )
        self.journal_button = Button(position=(10, self.map_button.rect.bottom + 10), image=journal_img, scale=2, split=3)
    
    def handle_event(self, event: pygame.event.Event):
        """Xử lý sự kiện cho các button"""
        self.map_button.handle_event(event=event)
    
    def update(self, delta_time: float = 0):
        """Cập nhật trạng thái UI"""
        # Update button states first
        self.menu_button.update()
        self.journal_button.update()
        self.map_button.update()
        
        # Check for menu button click
        if not self.menu_popup.is_open() and self.menu_button.was_clicked():
            self.menu_popup.toggle()
        
        # Update popup if open
        if self.menu_popup.is_open():
            self.menu_popup.update()

    def draw(self, screen: pygame.Surface):
        if self.menu_popup.is_open():
            self.menu_popup.draw(screen=screen)
        else:
            self.menu_button.draw(screen)
            self.journal_button.draw(screen)
            self.map_button.draw(screen)
